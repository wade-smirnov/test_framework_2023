import requests
from framework.clients.api_client import ApiClient


class etcdClient(ApiClient):
    url: str
    t_url: str
    d_internal_sso_username: str
    d_internal_sso_password: str

    @staticmethod
    def update_data_from_config() -> None:
        from framework.helpers.config_helper import get_config

        etcdClient.url = get_config("etcd_browser_url")
        etcdClient.t_url = get_config("etcd_t_url")
        etcdClient.d_internal_sso_username = get_config("d_internal_sso_username")
        etcdClient.d_internal_sso_password = get_config("d_internal_sso_password")

    @staticmethod
    def session_setup(
        stand_name: str,
        domain: str,
        d_internal_sso_username: str | None = None,
        d_internal_sso_password: str | None = None,
    ) -> None:
        etcdClient.url = f"http://{stand_name}.{domain}:8001"
        etcdClient.t_url = f"http://etcd.{stand_name}.{domain}:81"
        d_internal_sso_username = (
            d_internal_sso_username or etcdClient.d_internal_sso_username
        )
        d_internal_sso_password = (
            d_internal_sso_password or etcdClient.d_internal_sso_password
        )
        etcdClient.session = requests.Session()
        etcdClient.session.auth = (d_internal_sso_username, d_internal_sso_password)

    @staticmethod
    def session_auth_setup():
        etcdClient.session = requests.Session()
        etcdClient.session.auth = (
            etcdClient.d_internal_sso_username,
            etcdClient.d_internal_sso_password,
        )

    @staticmethod
    def get_nct_d_config_common_v2() -> dict:
        path = "/v2/keys/nct/co/config/common"
        response = etcdClient.get(path=path, status_code=200)
        return response.json()

    @staticmethod
    def get_nct_d_v2() -> dict:
        path = "/v2/keys/nct/co/?recursive=true"
        response = etcdClient.get(path=path, status_code=200)
        return response.json()

    @staticmethod
    def put_config_property(
        property_name: str, value: int, conf_path: str = "common"
    ) -> requests.Response:
        path = "/v2/keys/nct/co/config/" + conf_path + "/" + property_name
        params = {"value": value}
        response = etcdClient.put(path=path, status_code=200, params=params)
        return response
