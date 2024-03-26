from framework.clients.d_client import Client


class EtcdVerificator:
    @staticmethod
    def check_stand_status() -> None:
        core_status_data = Client.get_core_status()
        assert core_status_data.get("all") == "OK"
