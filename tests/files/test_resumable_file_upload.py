import allure
from framework.clients.d_client import Client
from framework.data.media_types import Mediatype
from framework.retry_decorator import retry_test
from framework.verificators.resumable_upload_verificator import (
    ResumableUploadVerificator,
)


@allure.title("Resumable file upload using TUS protocol")
class TestResumableUpload:
    """https://tus.io/protocols/resumable-upload"""

    @allure.testcase("Test full file upload using api/v1/files/uploadResumable")
    @retry_test()
    def test_resumable_upload_full_at_once(
        self, d_auth_token, jpeg_file_path, jpeg_file_binary_data, root_dir_id
    ):
        with allure.step("Preparing data for test"):
            filename = jpeg_file_path[jpeg_file_path.rfind("/") + 1:]  # fmt: skip
            file_length = str(len(jpeg_file_binary_data))

        with allure.step("Sending info about file to the server"):
            response = Client.post_upload_resumable_v1(
                upload_length=file_length,
                name=filename,
                type=Mediatype.jpeg,
                filetype=Mediatype.jpeg,
                filename=filename,
            )
            ResumableUploadVerificator.check_post_response(response=response)
            path = response.headers.get("location")

        with allure.step("Uploading full file"):
            upload_response = Client.patch_upload_resumable_v1(
                path=path, data=jpeg_file_binary_data
            )
            ResumableUploadVerificator.check_patch_response(
                response=upload_response, expected_upload_offset=file_length
            )

        with allure.step("Getting list of files, checking presence of uploaded one"):
            all_files_data_response = Client.get_files()
            file_data = ResumableUploadVerificator.check_file_existence(
                response=all_files_data_response,
                filename=filename,
                file_length=file_length,
            )
        with allure.step("Deleting file"):
            Client.delete_object(file_data.get("id"))

    @allure.testcase("Test upload file by parts using api/v1/files/uploadResumable")
    @retry_test()
    def test_resumable_file_upload_partial(
        self, jpeg_file_path, jpeg_file_binary_data, root_dir_id, d_auth_token
    ):
        with allure.step("Preparing file data for test"):
            filename = jpeg_file_path[jpeg_file_path.rfind("/") + 1:]  # fmt: skip
            file_length = str(len(jpeg_file_binary_data))
            first_part_of_file_length = int(file_length) // 2
            file_data_first_part = jpeg_file_binary_data[:first_part_of_file_length]
            file_data_second_part = jpeg_file_binary_data[first_part_of_file_length:]

        with allure.step("Sending info about file to the server"):
            file_data_response = Client.post_upload_resumable_v1(
                upload_length=file_length,
                name=filename,
                type=Mediatype.jpeg,
                filetype=Mediatype.jpeg,
                filename=filename,
            )
            ResumableUploadVerificator.check_post_response(response=file_data_response)
            path = file_data_response.headers.get("location")

        with allure.step("Uploading first part of the file"):
            upload_response = Client.patch_upload_resumable_v1(
                path=path, data=file_data_first_part
            )
            ResumableUploadVerificator.check_patch_response(
                response=upload_response,
                expected_upload_offset=str(first_part_of_file_length),
            )
        with allure.step("Getting Upload Offset"):
            middle_of_upload_response = Client.head_upload_resumable_v1(path=path)
            ResumableUploadVerificator.check_head_response(
                response=middle_of_upload_response,
                file_length=file_length,
                first_part_of_file_length=str(first_part_of_file_length),
            )

        with allure.step("Uploading second part of the file"):
            upload_response = Client.patch_upload_resumable_v1(
                path=path,
                data=file_data_second_part,
                upload_offset=str(first_part_of_file_length),
            )
            ResumableUploadVerificator.check_patch_response(
                response=upload_response, expected_upload_offset=file_length
            )

        with allure.step("Getting list of files, checking presence of uploaded one"):
            all_files_data_response = Client.get_files()
            file_data = ResumableUploadVerificator.check_file_existence(
                response=all_files_data_response,
                filename=filename,
                file_length=file_length,
            )
        with allure.step("Deleting file"):
            Client.delete_object(file_data.get("id"))

    @allure.testcase(
        "Test file upload stop and upload data delete api/v1/files/uploadResumable"
    )
    @retry_test()
    def test_resumable_file_upload_stop(
        self, jpeg_file_path, jpeg_file_binary_data, root_dir_id, d_auth_token
    ):
        with allure.step("Preparing file data for test"):
            filename = jpeg_file_path[jpeg_file_path.rfind("/") + 1:]  # fmt: skip
            file_length = str(len(jpeg_file_binary_data))
            first_part_of_file_length = int(file_length) // 2
            file_data_first_part = jpeg_file_binary_data[:first_part_of_file_length]
            file_data_second_part = jpeg_file_binary_data[first_part_of_file_length:]

        with allure.step("Sending info about file to the server"):
            file_data_response = Client.post_upload_resumable_v1(
                upload_length=file_length,
                name=filename,
                type=Mediatype.jpeg,
                filetype=Mediatype.jpeg,
                filename=filename,
            )
            ResumableUploadVerificator.check_post_response(response=file_data_response)
            path = file_data_response.headers.get("location")

        with allure.step("Uploading first part of the file"):
            upload_response = Client.patch_upload_resumable_v1(
                path=path, data=file_data_first_part
            )
            ResumableUploadVerificator.check_patch_response(
                response=upload_response,
                expected_upload_offset=str(first_part_of_file_length),
            )

        with allure.step("Stopping upload, deleting upload data"):
            Client.delete_upload_resumable_v1(path=path)
            Client.head_upload_resumable_v1(path=path, status_code=404)
            Client.patch_upload_resumable_v1(
                path=path,
                status_code=404,
                data=file_data_second_part,
                upload_offset=str(first_part_of_file_length),
            )

        with allure.step("Getting list of files, checking presence of file"):
            all_files_data_response = Client.get_files()
            ResumableUploadVerificator.check_file_existence(
                response=all_files_data_response,
                exist=False,
                filename=filename,
                file_length=file_length,
            )
