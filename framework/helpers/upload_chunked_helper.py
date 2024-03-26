from framework.clients.d_client import Client
from framework.clients.websocket_client import WebsocketClient
from framework.helpers.common_helpers import get_mediatype
from framework.helpers.upload_resumable_helper import UploadResumableHelper
from framework.utils import name_generator
from framework.verificators.websocket_verificator import WebSocketVerificator


class UploadChunkedHelper:
    @staticmethod
    def multy_upload_chunked_files_by_extension(
        extensions: list, dir_id: str, web_socket_client: WebsocketClient
    ):
        uploaded_files = {}
        for extension in extensions:
            file_path = UploadResumableHelper.get_file_path_by_extension(
                extension=extension, signature="embedded"
            )
            filename = name_generator(extension=extension)
            response = Client.post_upload_chunked(
                filename,
                file_path,
                get_mediatype(extension=extension),
                dir_id,
            )
            uploaded_files[extension] = {
                "id": Client.created_file_id,
                "filename": filename,
                "checksum": response.json().get("file").get("checksum"),
            }
            WebSocketVerificator.check_message_operation(
                Client.request_id,
                WebSocketVerificator.file_add,
                web_socket_client=web_socket_client,
            )
        return uploaded_files
