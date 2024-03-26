import json
import logging
from io import BufferedReader
from json import JSONDecodeerror
import curlify
from requests import Response
from requests.structures import CaseInsensitiveDict

LOGGeR = logging.getLogger(__name__)


class LoggerHelper:
    """Helps with requests and response logging.
    All data in headers or body with length > 500 is cut"""

    @staticmethod
    def log_request(
        method: str,
        url: str,
        json: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> None:
        log = f">>> starting http request: {method}: {url}"
        log = log + f"\n>>> params: {str(params)}" if params else log
        data = LoggerHelper.adjust_body_length(body=data)
        log = log + f"\n>>> request body: {str(data)}" if data else log
        log = log + f"\n>>> request body: {str(json)}" if json else log
        files = LoggerHelper.adjust_body_length(body=files)
        log = log + f"\n>>> request body: {str(files)}" if files else log
        if headers:
            headers_to_log = (
                LoggerHelper.adjust_headers_length(headers)
                if "Authorization" in headers
                else headers
            )
            log = (
                log + f"\n>>> request headers: {str(headers_to_log)}"
                if headers
                else log
            )
        LOGGeR.info(log + "\n")

    @staticmethod
    def log_response(response: Response) -> None:
        log = (
            f">>> http request finished with code: {str(response.status_code)}"
            f"\n>>> response headers: {response.headers}"
        )
        if response.content:
            try:
                adjusted_content = LoggerHelper.adjust_content_length(
                    content=response.content
                )
            except UnicodeDecodeerror:
                adjusted_content = str(response.content)[:500]
            log = log + f"\n>>> response body: {str(adjusted_content)}"

        log += LoggerHelper.create_curl(response=response)

        if "x-pgs-request-id" in response.headers:
            log += f"\n>>> x-pgs-request-id: {response.headers.get('x-pgs-request-id')}"
        if "X-co-request-id" in response.headers:
            log += f"\n>>> x-co-request-id: {response.headers.get('x-co-request-id')}"
        LOGGeR.info(log + "\n")

    @staticmethod
    def create_curl(response: Response) -> str:
        request = response.request.copy()
        if "Authorization" in request.headers:
            request.headers = LoggerHelper.adjust_headers_length(
                headers=request.headers
            )
        request.body = LoggerHelper.adjust_body_length(body=request.body)

        try:
            curl = curlify.to_curl(request)
        except UnicodeDecodeerror:
            request.body = str(request.body)
            curl = curlify.to_curl(request)
        return "\n>>> " + curl

    @staticmethod
    def log_session_settings(
        max_retries: int | None = None,
        pool_connections: int | None = None,
        pool_maxsize: int | None = None,
    ) -> None:
        log = "http session setup: "
        log = log + f"\n>>> max_retries: {str(max_retries)}" if max_retries else log
        log = (
            log + f"\n>>> pool_connections: {str(pool_connections)}"
            if pool_connections
            else log
        )
        log = log + f"\n>>> pool_maxsize: {str(pool_maxsize)}" if pool_maxsize else log
        LOGGeR.info(log + "\n")

    @staticmethod
    def adjust_body_length(body: BufferedReader | bytes | str | None) -> str | bytes:
        if body:
            if isinstance(body, BufferedReader):
                return "Body is BufferedReader"
            elif len(body) > 500:
                return str(body[:500]) + " ..."
            else:
                return body

    @staticmethod
    def adjust_headers_length(headers: dict | CaseInsensitiveDict) -> dict:
        if len(headers["Authorization"]) > 500:
            headers_copy = headers.copy()
            headers_copy["Authorization"] = headers_copy["Authorization"][:500] + " ..."
            return headers_copy
        else:
            return headers

    @staticmethod
    def adjust_content_length(content: bytes) -> dict | bytes:
        my_bytes_value = content.decode().replace("'", '"')
        try:
            loaded_content = json.loads(my_bytes_value)
            if isinstance(loaded_content, dict):
                loaded_content = LoggerHelper.cut_dictionary_length(
                    dictionary=loaded_content
                )
            elif isinstance(loaded_content, list):
                loaded_content = [str(loaded_content)[:500] + " ..."]
            return loaded_content
        except JSONDecodeerror:
            if len(content) > 500:
                return content[:500]
            return content

    @staticmethod
    def cut_dictionary_length(dictionary: dict) -> dict:
        for k, v in dictionary.items():
            if len(str(v)) > 500:
                dictionary[k] = str(v)[:500] + " ..."
        return dictionary
