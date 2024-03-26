import logging
import os

import pytest
from _pytest.config import Config
from filelock import FileLock
from framework.clients.e_client import eClient
from framework.helpers.e_helper import eHelper

from framework.clients.b_client import bClient
from framework.clients.d_client import Client
from framework.helpers.common_helpers import remove_temp_data
from framework.helpers.config_helper import (
    get_config,
    set_config_and_env_properties_data,
    update_clients_from_config,
)
from framework.helpers.upload_resumable_helper import UploadResumableHelper
from framework.utils import name_generator, get_timestamp_as_string

LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser) -> None:
    parser.addoption("--stand", action="store", default=None)
    parser.addoption("--launch", action="store", default=None)
    parser.addoption(
        "--t_user_password",
        action="store",
        default=None,
    )
    parser.addoption(
        "--t_admin_password",
        action="store",
        default=None,
    )
    parser.addoption(
        "--keycloak_password",
        action="store",
        default=None,
    )
    parser.addoption(
        "--keycloak_login",
        action="store",
        default=None,
    )
    parser.addoption(
        "--user_login",
        action="store",
        default=None,
    )
    parser.addoption(
        "--default_t",
        action="store",
        default=None,
    )

@pytest.fixture(scope="session", autouse=True)
def set_run_data(pytestconfig: Config, tmp_path_factory, worker_id) -> None:
    """Session scope is not working in parallel =>
    Config will be updated for every test =>
    to prevent this behaviour we check if config_status.txt exists,
    if it is not - we create it and update info, if exists we just get data"""

    config_data: dict = dict()
    # get the temp directory shared by all workers
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    config_status_file_path = root_tmp_dir / "config_status.txt"

    if worker_id == "master":
        LOGGER.info("Setting config for single thread run")
        config_data = set_config_and_env_properties_data(pytestconfig)
    else:
        LOGGER.info("Setting config for multi thread run")
        with FileLock(str(config_status_file_path) + ".lock"):
            if not config_status_file_path.is_file():
                config_data = set_config_and_env_properties_data(pytestconfig)
                config_status_file_path.write_text("Config is updated\n")
    update_clients_from_config()
    eHelper.e_token()
    eHelper.e_t()
    yield config_data
    if worker_id == "master":
        remove_temp_data(
            config_data=config_data,
            config_status_file_path=config_status_file_path,
        )
    else:
        worker_count = os.environ.get("PYTEST_XDIST_WORKER_COUNT")
        if int(worker_id[2:]) + 1 == worker_count:
            remove_temp_data(
                config_data=config_data,
                config_status_file_path=config_status_file_path,
            )


@pytest.fixture(scope="function", autouse=True)
def log_test(request) -> None:
    LOGGER.info(f"{request.node.nodeid}\n***** Test STARTED *****")
    yield
    LOGGER.info(f"{request.node.nodeid}\n***** Test FINISHED *****\n\n")


def pytest_configure(config):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    if worker_id is not None:
        with open(f"logs/tests_worker_{worker_id}.log", "w"):
            "cleaning log file"
        logging.basicConfig(
            format=config.getini("log_file_format"),
            filename=f"logs/tests_worker_{worker_id}.log",
            level=config.getini("log_file_level"),
        )


@pytest.fixture(scope="session")
def c_token(e_user) -> str:
    Client.post_auth(
        login=eClient.username,
        password=eClient.user_password,
    )
    return Client.token


@pytest.fixture(scope="function")
def c_token_function_scope(e_user) -> str:
    Client.post_auth(
        login=e_user,
        password=eClient.user_password,
    )
    Client.get_info()
    yield Client.token
    Client.post_auth(
        login=e_user,
        password=eClient.user_password,
    )
    Client.get_info()


@pytest.fixture(scope="session")
def b_token(e_user):
    return bClient.get_b_token(
        username=e_user, password=eClient.user_password
    )


@pytest.fixture(scope="session")
def e_user(
    pytestconfig: Config, tmp_path_factory, worker_id, username: None = None
) -> str:
    if worker_id == "master":
        LOGGER.info("Setting e user for single thread run")
        username = get_config("e_user_login")
        eClient.create_user(
            t_name=get_config("default_t"),
            username=username,
            status_code=(200, 409),
        )
    else:
        LOGGER.info("Setting e user for multi thread run")
        # get the temp directory shared by all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent

        fn = root_tmp_dir / f"worker_{worker_id}_status.txt"
        with FileLock(str(fn) + ".lock"):
            if not fn.is_file():
                username = worker_id + "-" + get_config("e_user_login")
                eClient.create_user(
                    t_name=get_config("default_t"),
                    username=username,
                    status_code=(200, 409),
                )
                fn.write_text("Worker is updated")
    return username


@pytest.fixture(scope="session")
def second_e_user(e_user, b_token):
    username = get_timestamp_as_string() + "-" + e_user
    eClient.domain = (
        get_config("default_t") + "." + eClient.storage_name + ".ru"
    )
    eClient.create_user(
        t_name=get_config("default_t"),
        username=username,
        status_code=(200, 409),
    )
    yield username
    try:
        user_id = eHelper.find_user_by_attribute(
            expected_attribute_value=username
        ).get("id")
        eClient.remove_user(user_id=user_id)
        eClient.create_user(
            t_name=get_config("default_t"),
            username=e_user,
            status_code=(200, 409),
        )
    except AttributeError:
        "User already removed"


@pytest.fixture(scope="session")
def root_dir_id(c_token):
    Client.get_info()
    return Client.root_dir_id


@pytest.fixture(scope="session")
def first_dir_id(c_token: str, root_dir_id: str) -> str:
    Client.get_info()
    Client.post_make_dir()
    first_dir_id = Client.created_dir_id
    yield first_dir_id
    Client.delete_object(first_dir_id, status_code=(204, 404))


@pytest.fixture(scope="function")
def reserve_dir_id(reserve_t) -> str:
    UploadResumableHelper.authorize_reserve_t(reserve_t=reserve_t)
    Client.get_info()
    Client.post_make_dir()
    dir_id = Client.created_dir_id
    yield dir_id
    Client.delete_object(dir_id, status_code=(204, 404))


@pytest.fixture(scope="session")
def second_dir_id(c_token: str, root_dir_id: str) -> str:
    Client.post_make_dir()
    second_dir_id = Client.created_dir_id
    yield second_dir_id
    Client.delete_object(second_dir_id, status_code=(204, 404))


@pytest.fixture
def enable_public_link(reserve_t):
    t_info = eClient.get_t_info()
    if not t_info.get("public_link_settings").get("public_link_enabled"):
        eHelper.set_t_public_link_property()
    t_info = eClient.get_t_info()
    yield t_info.get("public_link_settings").get("public_link_enabled")
    eHelper.set_t_public_link_property(enable=False)


@pytest.fixture
def disable_signature(reserve_t):
    UploadResumableHelper.authorize_reserve_t(reserve_t=reserve_t)
    eHelper.set_t_signature_property(
        signature_enabled=0, t_name=reserve_t.get("name")
    )
    yield
    eHelper.set_t_signature_property(
        signature_enabled=1, t_name=reserve_t.get("name")
    )


@pytest.fixture(scope="function")
def user_group(second_e_user):
    user_id = eHelper.find_user_by_attribute(
        expected_attribute_value=second_e_user
    ).get("id")
    group_name = name_generator(name="group")
    eClient.create_group(group_name=group_name)
    eClient.add_user_to_group(user_id=user_id)
    yield {"id": eClient.group_id, "name": eClient.group_name}
    eClient.delete_group(group_id=eClient.group_id)


