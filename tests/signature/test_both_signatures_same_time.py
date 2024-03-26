import allure
import pytest

from framework.clients.d_client import Client
from framework.helpers.common_helpers import get_mediatype
from framework.helpers.upload_resumable_helper import UploadResumableHelper
from framework.utils import name_generator
from framework.retry_decorator import retry_test
from framework.verificators.signature_verificator import SignatureVerificator


@allure.title("Test embedded and detached signatures on file at the same time")
class TestembeddedAndDetachedSignatureOnFile:
    @pytest.mark.skip  # 9307
    @pytest.mark.parametrize("password_protected", [True])
    @pytest.mark.parametrize("extension", [".odt", ".xlsx", ".docx"])
    @allure.testcase("Test setup of both signatures properties on one file")
    @retry_test()
    def test_both_signature_properties_setup_on_one_password_protected_file(
        self, root_dir_id, extension, password_protected
    ):
        with allure.step("Uploading file with embedded and detached signature"):
            file_path = UploadResumableHelper.get_file_path_by_extension(
                extension=extension,
                signature="both",
                password_protected=password_protected,
            )
            filename = name_generator(prefix="both", extension=extension)
            file_id = UploadResumableHelper.upload_file_without_changes(
                filename=filename,
                path_to_file=file_path,
                media_type=get_mediatype(extension=extension),
            )
            sig_file_path = file_path + ".sig"
            sig_file_name = filename + ".sig"
            sig_file_id = UploadResumableHelper.upload_file_without_changes(
                filename=sig_file_name,
                path_to_file=sig_file_path,
                media_type=get_mediatype(extension=extension),
            )
            with allure.step("Check signed properties"):
                response_json = Client.get_file_by_id(file_id).json()
                assert (
                    response_json.get("file").get("signatureInfo").get("hasembedded")
                ), "File's embedded signature is missing"
                SignatureVerificator.check_detached_signature_property_setup(
                    file_id=file_id, sig_file_id=sig_file_id
                )

            with allure.step("Removing detached signature"):
                Client.delete_object(object_id=sig_file_id)
                response_json = Client.get_file_by_id(file_id).json()
                assert (
                    response_json.get("file").get("signatureInfo").get("hasembedded")
                ), "File's embedded signature is missing"
                assert (
                    not response_json.get("file")
                    .get("signatureInfo")
                    .get("hasDetached")
                ), "File's detached signature is present"

            with allure.step("Post-requisites"):
                Client.delete_object(object_id=file_id)

    @pytest.mark.skip  # SRV-9307
    @pytest.mark.parametrize("password_protected", [False])
    @pytest.mark.parametrize("extension", [".odt", ".xlsx", ".docx"])
    @allure.testcase("Test setup of both signatures properties on one file")
    @retry_test()
    def test_both_signature_properties_setup_on_one_file(
        self, root_dir_id, extension, password_protected
    ):
        with allure.step("Uploading file with embedded and detached signature"):
            file_path = UploadResumableHelper.get_file_path_by_extension(
                extension=extension,
                signature="both",
                password_protected=password_protected,
            )
            filename = name_generator(prefix="both", extension=extension)
            file_id = UploadResumableHelper.upload_file_without_changes(
                filename=filename,
                path_to_file=file_path,
                media_type=get_mediatype(extension=extension),
            )
            sig_file_path = file_path + ".sig"
            sig_file_name = filename + ".sig"
            sig_file_id = UploadResumableHelper.upload_file_without_changes(
                filename=sig_file_name,
                path_to_file=sig_file_path,
                media_type=get_mediatype(extension=extension),
            )
            with allure.step("Check signed properties"):
                response_json = Client.get_file_by_id(file_id).json()
                assert (
                    response_json.get("file").get("signatureInfo").get("hasembedded")
                ), "File's embedded signature is missing"
                SignatureVerificator.check_detached_signature_property_setup(
                    file_id=file_id, sig_file_id=sig_file_id
                )

            with allure.step("Removing detached signature"):
                Client.delete_object(object_id=sig_file_id)
                response_json = Client.get_file_by_id(file_id).json()
                assert (
                    response_json.get("file").get("signatureInfo").get("hasembedded")
                ), "File's embedded signature is missing"
                assert (
                    not response_json.get("file")
                    .get("signatureInfo")
                    .get("hasDetached")
                ), "File's detached signature is present"

            with allure.step("Post-requisites"):
                Client.delete_object(object_id=file_id)
