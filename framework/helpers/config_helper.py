import yaml
from _pytest.config import Config
from yaml import SafeLoader
from framework.clients.etcd_client import EtcdClient


def prepare_data_for_config(pytestconfig: Config) -> dict:
    # Getting variables passed to pytest
    stand_name = pytestconfig.getoption("stand") or get_config("stand_name")
    domain = "myoffice-app.ru" if stand_name in ("pgscsi") else "devoffice.ru"  # noqa
    tenant_user_password = pytestconfig.getoption("tenant_user_password")
    tenant_admin_password = pytestconfig.getoption("tenant_admin_password")
    keycloak_password = pytestconfig.getoption("keycloak_password")
    keycloak_login = pytestconfig.getoption("keycloak_login")
    default_tenant = pytestconfig.getoption("default_tenant")
    co_internal_sso_username = pytestconfig.getoption("co_internal_sso_username")
    co_internal_sso_password = pytestconfig.getoption("co_internal_sso_password")
    launch = pytestconfig.getoption("launch")
    euclid_user_login = pytestconfig.getoption("euclid_user_login")

    # Getting storage name from ETCD
    storage_name = get_storage_name(
        stand_name=stand_name,
        domain=domain,
        co_internal_sso_username=co_internal_sso_username,
        co_internal_sso_password=co_internal_sso_password,
    )

    # Preparing login data to add/update in config
    data = dict()
    data["stand_name"] = stand_name or get_config("stand_name")
    data["co_internal_sso_username"] = co_internal_sso_username or get_config(
        "co_internal_sso_username"
    )
    data["co_internal_sso_password"] = co_internal_sso_password or get_config(
        "co_internal_sso_password"
    )
    data["tenant_user_password"] = tenant_user_password or get_config(
        "tenant_user_password"
    )
    data["tenant_admin_password"] = tenant_admin_password or get_config(
        "tenant_admin_password"
    )
    data["euclid_user_login"] = euclid_user_login or get_config("euclid_user_login")
    data["default_tenant"] = default_tenant or get_config("default_tenant")
    data["keycloak_password"] = keycloak_password or get_config("keycloak_password")
    data["keycloak_login"] = keycloak_login or get_config("keycloak_login")
    data["storage_name"] = storage_name or get_config("storage_name")
    data["domain"] = domain or get_config("domain")
    data["launch"] = launch or get_config("launch")
    data["co_admin_user"] = "admin@" + f"{data.get('default_tenant')}.{storage_name}.ru"

    # Preparing url data to add/update in config
    data["co_tenant_admin_url"] = f"https://admin-{stand_name}.devoffice.ru/#/login"
    data["etcd_browser_url"] = f"http://{stand_name}.{domain}:8001"
    data["co_auth_url"] = f"https://auth-{stand_name}.{domain}"
    data["co_api_url"] = f"https://coapi-{stand_name}.{domain}"
    data["co_admin_url"] = f"https://admin-{storage_name}.{domain}/adminapi"
    data["euclid_url"] = f"https://pgs-{storage_name}.{domain}/adminapi"
    data["aristotel_url"] = f"https://pgs-{storage_name}.{domain}/pgsapi"
    data["co_ws_url"] = f"wss://coapi-{stand_name}.{domain}/api/v1"
    data["etcd_tenant_url"] = f"http://etcd.{stand_name}.{domain}:81"
    return data


def get_stand_version_data() -> dict:
    parent_nodes = EtcdClient.get_nct_co_v2().get("node").get("nodes")
    versions = dict()
    for parent_node in parent_nodes:
        if parent_node.get("key") == "/nct/co/config":
            nodes = parent_node.get("nodes")
            for node in nodes:
                if node.get("key") == "/nct/co/config/versions":
                    for version in node.get("nodes"):
                        for component in ("dcm", "du", "pregen", "fm", "cvm"):
                            if component in version.get("key"):
                                versions[component+"_container_version"] = version.get(
                                    "value"
                                )  # fmt: skip
    return versions


def get_storage_name(
    stand_name: str,
    domain: str,
    co_internal_sso_username: str | None = None,
    co_internal_sso_password: str | None = None,
) -> str:
    """Receiving storage name from ETCD"""
    EtcdClient.update_data_from_config()
    EtcdClient.session_setup(
        stand_name=stand_name,
        domain=domain,
        co_internal_sso_username=co_internal_sso_username,
        co_internal_sso_password=co_internal_sso_password,
    )

    nodes = EtcdClient.get_nct_co_config_common_v2().get("node").get("nodes")
    for node in nodes:
        if node.get("key") == "/nct/co/config/common/fs.api.url":
            storage_url = node.get("value")
            storage_name = storage_url[12: storage_url.find("." + domain)]  # fmt: skip
            return storage_name


def write_data_to_config(data: dict) -> None:
    with open("./config.yaml", "r") as f:
        current_yaml = yaml.safe_load(f)
        for k, v in data.items():
            if k in current_yaml.items():
                current_yaml[k].update(v)
            else:
                current_yaml[k] = v

    if current_yaml:
        with open("./config.yaml", "w") as f:
            yaml.safe_dump(current_yaml, f)


def get_config(parameter: str) -> str:
    with open("./config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader) or {}
        return data.get(parameter)


def write_env_properties(data: dict, mode: str = "w") -> None:
    with open("tests/reports/environment.properties", mode) as f:
        data_to_write = ""
        for k, v in data.items():
            if "password" not in str(k):
                data_to_write += str(k) + "=" + str(v) + "\n"
        f.write(data_to_write)


def update_clients_from_config() -> None:
    from framework.clients.bclient import BClient
    from framework.clients.co_client import Client
    from framework.clients.etcd_client import EtcdClient
    from framework.clients.euclid_client import EuclidClient
    from framework.clients.co_admin_client import DClient

    EuclidClient.update_data_from_config()
    Client.update_data_from_config()
    EtcdClient.update_data_from_config()
    BClient.update_data_from_config()
    DClient.update_data_from_config()


def set_config_and_env_properties_data(pytestconfig: Config) -> dict:
    data = prepare_data_for_config(pytestconfig)
    write_data_to_config(data=data)
    versions = get_stand_version_data()
    write_env_properties(data=versions)
    write_env_properties(data=data, mode="a")
    return data
