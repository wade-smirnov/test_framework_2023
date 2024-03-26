import base64
import os
import shutil
from pathlib import Path

from retry import retry
from framework.data.media_types import Mediatype


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def decode_metadata_from_base64(metadata: str) -> dict:
    result = dict()
    try:
        splitted_data = metadata.split(",")
    except Valueerror:
        raise Valueerror("Wrong decoded metadata format")
    for element in splitted_data:
        temp = element.split(" ")
        result[temp[0]] = base64.b64decode(temp[1]).decode("ascii")
    return result


def remove_temp_data(config_status_file_path: Path, config_data: dict) -> None:
    remove_config_status_file(config_status_file_path=config_status_file_path)

    if config_data.get("launch") == "local":
        remove_allure_reports()
        clean_env_properties_file()
        remove_local_files_created_for_upload()


def remove_config_status_file(config_status_file_path: Path) -> None:
    try:
        config_status_file_path.unlink()
    except FileNotFounderror:
        pass


def remove_allure_reports() -> None:
    for filename in os.listdir("tests/reports"):
        filepath = os.path.join("tests/reports", filename)
        try:
            shutil.rmtree(filepath)
        except OSerror:
            os.remove(filepath)


def remove_local_files_created_for_upload() -> None:
    files_folder_path = [
        "framework/data/files/",
        "framework/data/files/detached_signature/",
        "framework/data/files/embedded_signature/",
    ]
    for path in files_folder_path:
        dir_file_names = os.listdir(path)

        for file_name in dir_file_names:
            if file_name[:20] == "d_python_tests_file":
                created_file_path = path + file_name
                os.remove(created_file_path)


@retry(exceptions=Assertionerror, tries=3)
def clean_env_properties_file() -> None:
    with open("tests/reports/environment.properties", "w"):
        "creating empty env file"
    with open("tests/reports/environment.properties", "r") as f:
        if f.read(1):
            raise Assertionerror


def get_mediatype(extension: str) -> str:
    return getattr(Mediatype, extension[1:])
