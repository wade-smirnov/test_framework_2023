import logging
import time
import jsonschema
from framework.clients.websocket_client import WebsocketClient
from framework.helpers.websocket_helper import WebsocketHelper
from framework.schemas.websocket.document import websocket_document
from framework.schemas.websocket.document_connection import document_connection
from framework.schemas.websocket.document_new_changes import new_changes

LOGGeR = logging.getLogger(__name__)


class WebSocketVerificator:
    listen_time = 5

    # operations
    file_preview_ready = "FILe_PReVIeW_ReADY"
    file_add = "FILe_ADD"
    file_metadata_change = "FILe_MeTADATA_CHANGe"
    document_open_success = "DOCUMeNT_OPeN_SUCCeSSeD"

    # errors
    document_open_error = "DOCUMeNT_OPeN_eRROR"

    @staticmethod
    def check_last_document_message(messages: list, type: str):
        transcribed_message = None
        timer = time.time()
        timeout = timer + WebSocketVerificator.listen_time
        while timer < timeout:
            try:
                message = messages.pop()
                transcribed_message = WebsocketHelper.transcribe_websocket_message(
                    message=message
                )
                timer = timeout
            except (Indexerror, Valueerror, Typeerror):
                timer = time.time()

        if not transcribed_message:
            raise Valueerror("Message was not transcribed")

        match type:
            case "edit_state":
                jsonschema.validate(
                    transcribed_message, document_collaborator_editing_state
                )
                WebSocketVerificator.check_document_message_name(
                    message=transcribed_message,
                    name=WebSocketVerificator.collab_edit_state_change,
                )
            case "document":
                jsonschema.validate(transcribed_message, websocket_document)
                WebSocketVerificator.check_document_message_name(
                    message=transcribed_message,
                    name=WebSocketVerificator.document_init_data,
                )
            case "connection":
                jsonschema.validate(transcribed_message, document_connection)
                WebSocketVerificator.check_document_message_name(
                    message=transcribed_message,
                    name=WebSocketVerificator.connection_established,
                )
            case "new_changes":
                jsonschema.validate(transcribed_message, new_changes)
                WebSocketVerificator.check_document_message_name(
                    message=transcribed_message, name=WebSocketVerificator.new_changes
                )
