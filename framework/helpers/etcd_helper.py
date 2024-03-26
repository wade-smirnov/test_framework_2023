import time
from jsonschema.exceptions import ValidationError
from framework.clients.etcd_client import EtcdClient
from framework.utils import wait
from framework.verificators.etcd_verificator import EtcdVerificator


class EtcdHelper:
    @staticmethod
    def change_etcd_settings(
        component: str, property_name: str, value: int | str | None = None
    ) -> None:
        EtcdVerificator.check_stand_status()
        EtcdClient.put_config_property(
            conf_path=component, property_name=property_name, value=value
        )
        wait(30, "Component restart")

        # Making sure stand status is OK
        timer = time.time()
        timeout = timer + 30
        while timer < timeout:
            try:
                wait(1, "Check stand health")
                EtcdVerificator.check_stand_status()
                break
            except ValidationError:
                pass
        EtcdVerificator.check_stand_status()
