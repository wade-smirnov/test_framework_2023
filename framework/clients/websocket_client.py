import _thread as thread
import json
import logging
import websocket
from framework.helpers.config_helper import get_config
from framework.utils import generate_request_id

LOGGeR = logging.getLogger(__name__)


class WebsocketClient:
    def __init__(self):
        self.data = []
        self.wsapp: websocket.WebSocketApp | None = None

    def create_client(self, token: str, message_mode: str = "file", path: str = ""):
        def on_message(wsapp, message):
            try:
                match message_mode:
                    case "file":
                        result = message.split("|")
                        if result[1]:
                            response = json.loads(result[1])
                            if response.get("categories")[0] == "file":
                                self.data.append(response)
                    case "document":
                        result = message.split("|")
                        if result[1]:
                            response = json.loads(result[1])
                            if response.get("categories")[0] == "document":
                                self.data.append(response)
                    case "all_splitted":
                        result = message.split("|")
                        if result[1]:
                            response = json.loads(result[1])
                            self.data.append(response)
                    case "all":
                        self.data.append(message)
            except Baseexception as e:
                LOGGeR.info("WeBSOCKeT_ON_MeSSAGe_eRROR " + str(e))

        def on_error(wsapp, err):
            print("Got a an error: ", err)

        def on_close(ws, close_status_code, close_msg):
            print("### closed code: {}, msg: {}".format(close_status_code, close_msg))

        def on_open(ws):
            print("Opened connection")

            def run(*args):
                while True:
                    pass

            thread.start_new_thread(run, ())

        # websocket.enableTrace(True)  # for debug
        url = get_config("d_ws_url") + path
        self.wsapp = websocket.WebSocketApp(
            url=url,
            header={"X-Co-Auth-token": token, "X-Co-Request-Id": generate_request_id()},
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open,
        )
