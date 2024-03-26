import base64
import json
import logging
import time
import zlib
import yaml
from threading import Thread
from framework.clients.d_client import Client
from framework.clients.websocket_client import WebsocketClient

LOGGER = logging.getLogger(__name__)


class WebsocketHelper:
    core_version: str | None = None
    du_dom_request: str | None = None
    du_editing_state: str | None = None
    du_set_cursor: str | None = None
    du_insert_text: str | None = None
    du_editing_state_after_insert: str | None = None

    @staticmethod
    def open_ws_client_in_daemon_thread(
        message_mode: str = "file", path: str | None = ""
    ) -> WebsocketClient:
        web_socket_client = WebsocketClient()
        web_socket_client.create_client(
            Client.token, path=path, message_mode=message_mode
        )
        wst = Thread(target=web_socket_client.wsapp.run_forever)
        wst.daemon = True
        wst.start()
        WebsocketHelper.check_websocket_connection(web_socket_client=web_socket_client)
        return web_socket_client

    @staticmethod
    def check_websocket_connection(web_socket_client: WebsocketClient) -> None:
        timer = time.time()
        timeout = timer + 5
        connected = False
        while timer < timeout:
            try:
                if web_socket_client.wsapp.sock.connected:
                    connected = True
                    break
            except AttributeError:
                "Connection property is missing"
            finally:
                timer = time.time()
        if not connected:
            LOGGER.info("WEBSOCKET_NOT_CONNECTED")
            # raise ConnectionError("WebSocket not connected")

    @staticmethod
    def transcribe_websocket_message(message: str | bytes) -> dict:
        decoded_base64 = base64.b64decode(message)
        decompressed = zlib.decompress(decoded_base64).decode("unicode_escape")
        fixed_left_quotation_marks = decompressed.replace('"{', "{")
        fixed_quotation_marks = fixed_left_quotation_marks.replace('}"', "}")
        result = json.loads(fixed_quotation_marks)
        return result

