import os
import pytest
from framework.clients.euclid_client import EuclidClient
from framework.etcd_settings import EtcdSettings
from framework.helpers.etcd_helper import EtcdHelper
from framework.helpers.euclid_helper import EuclidHelper
from framework.helpers.upload_resumable_helper import UploadResumableHelper


@pytest.fixture
def restore_redis_tus_ttl() -> None:
    yield
    EtcdHelper.change_etcd_settings(
        component="fm",
        property_name="redis.tus.ttlSecs",
        value=EtcdSettings.redis_tus_ttlSecs,
    )


@pytest.fixture
def restore_default_user_quota_after_test(euclid_user: str) -> None:
    yield
    user_id = EuclidHelper.find_user_by_attribute(
        attribute_name="username", expected_attribute_value=euclid_user
    ).get("id")
    EuclidClient.update_user_quota(quota=1000000000, user_id=user_id)


@pytest.fixture
def jpeg_file_path() -> str:
    file = UploadResumableHelper.find_file_by_extension(".jpeg")
    created_file_path = UploadResumableHelper.prepare_file_for_upload(file=file)
    yield created_file_path
    # Removing file after test
    try:
        os.remove(created_file_path)
    except FileNotFoundError:
        "Already removed"


@pytest.fixture
def jpeg_file_binary_data(jpeg_file_path: str) -> bytes:
    with open(file=jpeg_file_path, mode="rb") as f:
        data = f.read()
    return data
