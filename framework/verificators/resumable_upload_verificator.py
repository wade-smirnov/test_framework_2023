import requests
from framework.clients.d_client import Client


class ResumableUploadVerificator:
    @staticmethod
    def check_tus_protocol_version(response: requests.Response) -> None:
        assert (
            response.headers.get("Tus-Resumable") == Client.tus_version
        ), "Received version of Tus Protocol is not matching expected one"

    @staticmethod
    def check_content_length(response: requests.Response) -> None:
        received_content_length = response.headers.get("Content-Length")
        assert received_content_length == str(0), (
            f"Received content length {received_content_length} "
            f"is not matching expected one {str(0)}"
        )

    @staticmethod
    def check_upload_offset(
        response: requests.Response, expected_upload_offset: str
    ) -> None:
        received_upload_offset = response.headers.get("Upload-Offset")
        assert received_upload_offset == expected_upload_offset, (
            f"Received upload offset {received_upload_offset} "
            f"is not matching expected one {expected_upload_offset}"
        )

    @staticmethod
    def check_post_response(response: requests.Response) -> None:
        ResumableUploadVerificator.check_content_length(response)
        ResumableUploadVerificator.check_tus_protocol_version(response)

        path = response.headers.get("location")
        assert path, "path for upload and file_id were not returned"

        expected_path = "/api/v1/files/uploadResumable/"
        assert path[:30] == expected_path, (
            f"Path for upload {path[:30]}, "
            f"is not matching expected one {expected_path}"
        )

    @staticmethod
    def check_patch_response(
        response: requests.Response, expected_upload_offset: str
    ) -> None:
        ResumableUploadVerificator.check_upload_offset(
            response=response, expected_upload_offset=expected_upload_offset
        )
        ResumableUploadVerificator.check_tus_protocol_version(response)

    @staticmethod
    def check_head_response(
        response: requests.Response, file_length: str, first_part_of_file_length: str
    ) -> None:
        ResumableUploadVerificator.check_tus_protocol_version(response)
        ResumableUploadVerificator.check_upload_offset(
            expected_upload_offset=first_part_of_file_length, response=response
        )
        upload_length = response.headers.get("Upload-Length")
        assert upload_length == file_length, (
            f"Received upload length {upload_length} "
            f"is not matching expected one {file_length}"
        )

    @staticmethod
    def check_file_existence(
        response: requests.Response | dict,
        exist: bool = True,
        file_id: str | None = None,
        filename: str | None = None,
        file_length: str | None = None,
    ) -> dict | None:
        search_element = ""
        search_value = ""

        if file_id:
            search_element = "id"
            search_value = file_id
        elif filename:
            search_element = "filename"
            search_value = filename

        found_file = None
        for file_data in response:
            if file_data.get("file").get(search_element) == search_value:
                found_file = file_data.get("file")
                break
        if exist:
            assert search_value == found_file.get(
                search_element
            ), f"Uploaded file ({search_value}) is not found in the folder"
            assert file_length == found_file.get(
                "fileSize"
            ), f"Uploaded file ({file_length}) is not found in the folder"
            return found_file
        else:
            if found_file:
                raise Assertionerror("File found in the folder")
