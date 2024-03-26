import requests
from framework.clients.api_client import ApiClient


class EtcdClient(ApiClient):
    url: str
    tenant_url: str
    co_internal_sso_username: str
    co_internal_sso_password: str

    @staticmethod
    def update_data_from_config() -> None:
        from framework.helpers.config_helper import get_config

        EtcdClient.url = get_config("etcd_browser_url")
        EtcdClient.tenant_url = get_config("etcd_tenant_url")
        EtcdClient.co_internal_sso_username = get_config("co_internal_sso_username")
        EtcdClient.co_internal_sso_password = get_config("co_internal_sso_password")

    @staticmethod
    def session_setup(
        stand_name: str,
        domain: str,
        co_internal_sso_username: str | None = None,
        co_internal_sso_password: str | None = None,
    ) -> None:
        EtcdClient.url = f"http://{stand_name}.{domain}:8001"
        EtcdClient.tenant_url = f"http://etcd.{stand_name}.{domain}:81"
        co_internal_sso_username = (
            co_internal_sso_username or EtcdClient.co_internal_sso_username
        )
        co_internal_sso_password = (
            co_internal_sso_password or EtcdClient.co_internal_sso_password
        )
        EtcdClient.session = requests.Session()
        EtcdClient.session.auth = (co_internal_sso_username, co_internal_sso_password)

    @staticmethod
    def session_auth_setup():
        EtcdClient.session = requests.Session()
        EtcdClient.session.auth = (
            EtcdClient.co_internal_sso_username,
            EtcdClient.co_internal_sso_password,
        )

    @staticmethod
    def get_nct_co_config_common_v2() -> dict:
        path = "/v2/keys/nct/co/config/common"
        response = EtcdClient.get(path=path, status_code=200)
        return response.json()

    @staticmethod
    def get_nct_co_v2() -> dict:
        path = "/v2/keys/nct/co/?recursive=true"
        response = EtcdClient.get(path=path, status_code=200)
        return response.json()

    @staticmethod
    def put_config_property(
        property_name: str, value: int, conf_path: str = "common"
    ) -> requests.Response:
        path = "/v2/keys/nct/co/config/" + conf_path + "/" + property_name
        params = {"value": value}
        response = EtcdClient.put(path=path, status_code=200, params=params)
        return response

    @staticmethod
    def delete_tenant_settings_from_etcd(
        tenant_id: str,
    ) -> requests.Response:
        EtcdClient.session_auth_setup()
        path = "/v2/keys/nct/co/tenants/" + tenant_id
        url = EtcdClient.tenant_url + path
        response = EtcdClient.delete(url=url, status_code=200)
        return response
