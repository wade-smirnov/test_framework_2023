import os
import time
from random import randint
from retry import retry
from framework.clients.bclient import BClient
from framework.clients.co_client import Client
from framework.helpers.common_helpers import get_mediatype
from framework.utils import generate_file_name
from framework.verificators.resumable_upload_verificator import (
    ResumableUploadVerificator,
)


class UploadResumableHelper:
    files_folder_path: str = "framework/data/files/"

    @staticmethod
    def upload_file_without_changes(
        filename: str, path_to_file: str, media_type: str
    ) -> str:
        with open(path_to_file, "rb") as f:
            data = f.read()
        file_length = str(len(data))
        response = Client.post_upload_resumable_v1(
            upload_length=file_length,
            name=filename,
            type=media_type,
            filetype=media_type,
            filename=filename,
        )
        ResumableUploadVerificator.check_post_response(response=response)
        path = response.headers.get("location")
        upload_response = Client.patch_upload_resumable_v1(path=path, data=data)
        ResumableUploadVerificator.check_patch_response(
            response=upload_response, expected_upload_offset=file_length
        )
        file_data = UploadResumableHelper.check_file_exist_in_root_folder(
            filename=filename, file_length=file_length
        )

        Client.created_file_id = file_data.get("id")
        return file_data.get("id")

    @staticmethod
    def upload_file_with_detached_signarure(extension: str, filename: str) -> tuple:
        file_path = UploadResumableHelper.get_file_path_by_extension(
            extension=extension, signature="detached"
        )
        file_id = UploadResumableHelper.upload_file_without_changes(
            filename=filename,
            path_to_file=file_path,
            media_type=get_mediatype(extension=extension),
        )
        sig_filename = filename + ".sig"
        sig_file_path = file_path + ".sig"
        sig_file_id = UploadResumableHelper.upload_file_without_changes(
            filename=sig_filename,
            path_to_file=sig_file_path,
            media_type=get_mediatype(extension=".sig"),
        )
        return file_id, sig_file_id

    @staticmethod
    @retry(tries=3, delay=1)
    def check_file_exist_in_root_folder(filename: str, file_length: str) -> dict:
        all_files_data_response = Client.get_files()
        file_data = ResumableUploadVerificator.check_file_existence(
            response=all_files_data_response,
            filename=filename,
            file_length=file_length,
        )
        return file_data

    @staticmethod
    def find_file_by_extension(extension: str, path: str | None = None) -> str:
        path = path or UploadResumableHelper.files_folder_path
        dir_file_names = os.listdir(path)
        selected_files = []
        for file_name in dir_file_names:
            if file_name[-len(extension) :] == extension:  # noqa
                selected_files.append(file_name)
        if len(selected_files) > 0:
            index = randint(0, len(selected_files) - 1)
            return selected_files[index]
        else:
            raise FileNotFoundError("File for upload was not found")

    @staticmethod
    def prepare_file_for_upload(
        file: str, path: str | None = None, copy_file_name: str | None = None
    ) -> str:
        path = path or UploadResumableHelper.files_folder_path
        extension = "." + file.rsplit(".")[1]
        copy_file_name = copy_file_name or generate_file_name(extension)
        created_file_path = path + copy_file_name
        command = f"cp {path + file} {created_file_path}"
        os.popen(command)
        timer = time.time()
        timeout = timer + 15
        while timer < timeout:
            if os.path.exists(created_file_path):
                break
            else:
                timer = time.time()
        return created_file_path

    @staticmethod
    def get_file_path_by_extension(
        extension: str,
        signature: str | None = None,
        correct_format: bool = True,
        password_protected: bool = False,
    ) -> str:
        """Find file, return path to it"""
        if signature == "embedded" and password_protected:
            path = "framework/data/files/embedded_signature/password_protected/"
        elif signature == "embedded":
            path = "framework/data/files/embedded_signature/"
        elif signature == "detached" and password_protected:
            path = "framework/data/files/detached_signature/password_protected/"
        elif signature == "detached" and correct_format:
            path = "framework/data/files/detached_signature/correct_format/"
        elif signature == "detached":
            path = "framework/data/files/detached_signature/incorrect_format/"
        elif signature == "both" and password_protected:
            path = "framework/data/files/both_signatures/password_protected/"
        elif signature == "both":
            path = "framework/data/files/both_signatures/"
        else:
            path = "framework/data/files/"
        filename = UploadResumableHelper.find_file_by_extension(
            extension=extension,
            path=path,
        )
        return path + filename

    @staticmethod
    def authorize_reserve_tenant(reserve_tenant: dict):
        Client.post_auth(
            login=reserve_tenant.get("username"),
            password=reserve_tenant.get("user_password"),
        )
        Client.get_info()
        BClient.get_aristotel_token(
            username=reserve_tenant.get("username"),
            password=reserve_tenant.get("user_password"),
        )
