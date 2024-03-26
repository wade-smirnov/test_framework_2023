import yaml
from _pytest.config import Config
from yaml import SafeLoader
from framework.clients.etcd_client import etcdClient


def prepare_data_for_config(pytestconfig: Config) -> dict:
    # Getting variables passed to pytest
    stand_name = pytestconfig.getoption("stand") or get_config("stand_name")
    launch = pytestconfig.getoption("launch")
    e_user_login = pytestconfig.getoption("e_user_login")

    # Getting storage name from eTCD
    storage_name = get_storage_name(
        stand_name=stand_name,
    )

    # Preparing login data to add/update in config
    data = dict()
    data["stand_name"] = stand_name or get_config("stand_name")

    # Preparing url data to add/update in config
    data["d_tenant_admin_url"] = f"https://admin-{stand_name}.devoffice.ru/#/login"
    return data


def get_storage_name(
    stand_name: str,
    domain: str,
    d_internal_sso_username: str | None = None,
    d_internal_sso_password: str | None = None,
) -> str:
    """Receiving storage name from eTCD"""
    etcdClient.update_data_from_config()
    etcdClient.session_setup(
        stand_name=stand_name,
        domain=domain,
        d_internal_sso_username=d_internal_sso_username,
        d_internal_sso_password=d_internal_sso_password,
    )

    nodes = etcdClient.get_nct_d_config_common_v2().get("node").get("nodes")
    for node in nodes:
        if node.get("key") == "/nct/co/config/common/fs.api.url":
            storage_url = node.get("value")
            storage_name = storage_url[12: storage_url.find("." + domain)]  # fmt: skip
            return storage_name


def write_data_to_config(data: dict) -> None:
    with open("./config.yaml", "r") as f:
        current_yaml = yaml.safe_load(f)
        for k, v in data.items():
            if k in current_yaml.items():
                current_yaml[k].update(v)
            else:
                current_yaml[k] = v

    if current_yaml:
        with open("./config.yaml", "w") as f:
            yaml.safe_dump(current_yaml, f)


def get_config(parameter: str) -> str:
    with open("./config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader) or {}
        return data.get(parameter)


def write_env_properties(data: dict, mode: str = "w") -> None:
    with open("tests/reports/environment.properties", mode) as f:
        data_to_write = ""
        for k, v in data.items():
            if "password" not in str(k):
                data_to_write += str(k) + "=" + str(v) + "\n"
        f.write(data_to_write)


def update_clients_from_config() -> None:
    from framework.clients.b_client import BClient
    from framework.clients.d_client import Client
    from framework.clients.etcd_client import etcdClient
    from framework.clients.e_client import eClient
    from framework.clients.d_admin_client import DClient

    eClient.update_data_from_config()
    Client.update_data_from_config()
    etcdClient.update_data_from_config()
    BClient.update_data_from_config()
    DClient.update_data_from_config()


def set_config_and_env_properties_data(pytestconfig: Config) -> dict:
    data = prepare_data_for_config(pytestconfig)
    write_data_to_config(data=data)
    versions = get_stand_version_data()
    write_env_properties(data=versions)
    write_env_properties(data=data, mode="a")
    return data
