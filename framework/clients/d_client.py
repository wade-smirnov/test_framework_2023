import base64
import requests
from framework.clients.api_client import ApiClient
from framework.helpers.config_helper import get_config
from framework.utils import generate_request_id


class Client(ApiClient):
    url: str
    token: str
    auth_url: str
    root_dir_id: str
    d_user: str
    d_password: str
    request_id: str
    created_dir_id: str
    created_file_id: str

    @staticmethod
    def update_data_from_config() -> None:
        Client.url = get_config("d_api_url")
        Client.auth_url = get_config("d_auth_url")
        Client.d_internal_sso_username = get_config("d_internal_sso_username")
        Client.d_internal_sso_password = get_config("d_internal_sso_password")
        Client.d_user = get_config("e_user_login")
        Client.d_password = get_config("e_admin_password")

    @staticmethod
    def post_auth(
        login: str | None = None, password: str | None = None, status_code: int = 200
    ) -> dict:
        login = login or get_config("e_user_login")
        password = password or get_config("t_user_password")
        path = "/login"
        url = Client.auth_url + path
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = {"login": login, "password": password}
        response = Client.post(
            path=path, json=data, url=url, status_code=status_code, headers=headers
        ).json()
        Client.token = response.get("token")
        return response

    @staticmethod
    def post_logout(status_code: int = 200) -> dict:
        path = "/logout"
        url = Client.auth_url + path
        data = {"token": Client.token}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = Client.post(
            path=path, json=data, url=url, status_code=status_code, headers=headers
        )
        return response.json()

    @staticmethod
    def post_auth_ticket(status_code: int = 200, request_id: str | None = None) -> dict:
        path = "/api/v1/auth/ticket"
        url = Client.url + path
        Client.request_id = request_id or generate_request_id()
        headers = {
            "X-co-auth-token": Client.token,
            "X-co-request-id": Client.request_id,
            "Accept": "application/json",
        }
        response = Client.post(
            path=path, url=url, status_code=status_code, headers=headers
        ).json()
        return response

    @staticmethod
    def get_core_version_v1(
        status_code: int = 200, request_id: str | None = None
    ) -> dict:
        path = "/api/v1/documents/coreVersion"
        Client.request_id = request_id or generate_request_id()
        headers = {
            "X-co-auth-token": Client.token,
            "X-co-request-id": request_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = Client.get(path=path, status_code=status_code, headers=headers)
        return response.json()

    @staticmethod
    def get_core_status(status_code: int = 200) -> dict:
        path = ":8443/api/manage/core/status"
        Client.session.auth = (
            Client.d_internal_sso_username,
            Client.d_internal_sso_password,
        )
        response = Client.get(path=path, status_code=status_code)
        Client.session.auth = None
        return response.json()

    @staticmethod
    def options_upload_resumable_v1(
        status_code: int = 204, data: dict | None = None, request_id: str | None = None
    ) -> requests.Response:
        request_id = request_id or generate_request_id()
        path = "/api/v1/files/uploadResumable"
        headers = {
            "Tus-Resumable": Client.tus_version,
            "X-Co-Auth-Token": Client.token,
            "X-Co-Request-Id": request_id,
        }
        response = Client.options(
            path=path, headers=headers, data=data, status_code=status_code
        )
        return response

    @staticmethod
    def post_upload_resumable_v1(
        name: str,
        type: str,  # noqa
        filetype: str,
        filename: str,
        upload_length: str,
        status_code: int = 201,
        convert: str = "False",
        synchronous: str = "False",
        request_id: str | None = None,
        parent_folder_id: str | None = None,
        timezoneOffsetMins: str = str(0),  # noqa
        ignoreQuotaCheck: str = "False",  # noqa
    ) -> requests.Response:
        parent_folder_id = parent_folder_id or Client.root_dir_id
        for k, v in locals().items():
            if k not in (
                "data",
                "status_code",
                "request_id",
                "metadata",
                "parent_folder_id",
            ):
                v = base64.b64encode(bytes(v, encoding="utf-8"))

        path = "/api/v1/files/uploadResumable"
        headers = {
            "Tus-Resumable": Client.tus_version,
            "X-co-auth-token": Client.token,
            "Content-Length": str(0),
            "Upload-Length": upload_length,
            "X-Co-Request-Id": request_id,
        }
        response = Client.post(path=path, headers=headers, status_code=status_code)
        return response
