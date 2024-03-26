import os
import pytest
from framework.clients.e_client import eClient
from framework.etcd_settings import etcdSettings
from framework.helpers.etcd_helper import etcdHelper
from framework.helpers.e_helper import eHelper
from framework.helpers.upload_resumable_helper import UploadResumableHelper


@pytest.fixture
def restore_redis_tus_ttl() -> None:
    yield
    etcdHelper.change_etcd_settings(
        component="fm",
        property_name="redis.tus.ttlSecs",
        value=etcdSettings.redis_tus_ttlSecs,
    )


@pytest.fixture
def restore_default_user_quota_after_test(e_user: str) -> None:
    yield
    user_id = eHelper.find_user_by_attribute(
        attribute_name="username", expected_attribute_value=e_user
    ).get("id")
    eClient.update_user_quota(quota=1000000000, user_id=user_id)


@pytest.fixture
def jpeg_file_path() -> str:
    file = UploadResumableHelper.find_file_by_extension(".jpeg")
    created_file_path = UploadResumableHelper.prepare_file_for_upload(file=file)
    yield created_file_path
    # Removing file after test
    try:
        os.remove(created_file_path)
    except FileNotFounderror:
        "Already removed"


@pytest.fixture
def jpeg_file_binary_data(jpeg_file_path: str) -> bytes:
    with open(file=jpeg_file_path, mode="rb") as f:
        data = f.read()
    return data
