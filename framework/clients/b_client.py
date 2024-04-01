import json
import requests
from framework.clients.api_client import ApiClient
from framework.helpers.config_helper import get_config


class BClient(ApiClient):
    token: str
    username: str
    root_dir_id: str
    user_password: str
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    @staticmethod
    def update_data_from_config() -> None:
        BClient.username = get_config("e_user_login")
        BClient.user_password = get_config("t_user_password")
        BClient.url = get_config("aristotel_url")

    @staticmethod
    def get_b_token(
        status_code: int = 200,
        username: str | None = None,
        password: str | None = None,
    ) -> dict:
        login = username or BClient.username
        password = password or BClient.user_password
        data = {
            "login": login,
            "password": password,
        }
        response = BClient.post(
            data=data,
            path="/?cmd=auth",
            headers=BClient.headers,
            status_code=status_code,
        ).json()
        BClient.token = response["response"]["token"]
        return response

    @staticmethod
    def get_personal_data(status_code: int = 200) -> requests.Response:
        data = {"token": BClient.token}
        response = BClient.post(
            path="/?cmd=get_personal_data",
            data=data,
            headers=BClient.headers,
            status_code=status_code,
        )
        BClient.root_dir_id = (
            response.json().get("response").get("special_dirs").get("root_dir")
        )
        return response

    @staticmethod
    def get_props(file_id: str, status_code: int = 200) -> dict:
        data = {"token": BClient.token, "id": file_id}
        response = BClient.post(
            path="/?cmd=get_props",
            data=data,
            headers=BClient.headers,
            status_code=status_code,
        )
        return response.json().get("response")

    @staticmethod
    def change_property(props: dict, file_id: str, status_code: int = 200):
        props = json.dumps(props)
        data = {
            "token": BClient.token,
            "cmd": "set_props",
            "id": file_id,
            "props": props,
        }
        response = BClient.post(data=data, status_code=status_code)
        return response
