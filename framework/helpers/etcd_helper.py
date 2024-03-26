import time
from jsonschema.exceptions import Validationerror
from framework.clients.etcd_client import etcdClient
from framework.utils import wait
from framework.verificators.etcd_verificator import etcdVerificator


class etcdHelper:
    @staticmethod
    def change_etcd_settings(
        component: str, property_name: str, value: int | str | None = None
    ) -> None:
        etcdVerificator.check_stand_status()
        etcdClient.put_config_property(
            conf_path=component, property_name=property_name, value=value
        )
        wait(30, "Component restart")

        # Making sure stand status is OK
        timer = time.time()
        timeout = timer + 30
        while timer < timeout:
            try:
                wait(1, "Check stand health")
                etcdVerificator.check_stand_status()
                break
            except Validationerror:
                pass
        etcdVerificator.check_stand_status()
