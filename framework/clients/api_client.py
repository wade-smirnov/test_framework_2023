from __future__ import annotations
from typing import Type
import requests
from requests import Session, adapters
from framework.helpers.common_helpers import Singleton
from framework.helpers.logging_helper import LoggerHelper
from framework.verificators.common_verificators import status_code_check


class ApiClient(metaclass=Singleton):
    url: str
    session: Session = requests.Session()

    @classmethod
    def configure_session(
        cls: Type[ApiClient],
        max_retries: int = 3,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
    ) -> None:
        LoggerHelper.log_session_settings(
            max_retries=max_retries,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
        )
        adapter = adapters.HTTPAdapter(
            max_retries=max_retries,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
        )
        cls.session.mount("https://", adapter)
        cls.session.mount("http://", adapter)

    @classmethod
    @status_code_check
    def get(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(method="get", url=url, params=params, headers=headers)
        response = cls.session.request(
            method="get",
            url=url,
            params=params,
            headers=headers,
        )
        LoggerHelper.log_response(response=response)
        return response

    @classmethod
    @status_code_check
    def post(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        files: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "co_python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(
            method="post", url=url, data=data, headers=headers, json=json, params=params
        )
        response = cls.session.request(
            method="post",
            url=url,
            data=data,
            headers=headers,
            json=json,
            files=files,
            params=params,
        )
        LoggerHelper.log_response(response=response)
        return response

    @classmethod
    @status_code_check
    def patch(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "co_python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(
            method="patch",
            url=url,
            data=data,
            headers=headers,
            json=json,
            params=params,
        )
        response = cls.session.request(
            method="patch",
            url=url,
            data=data,
            headers=headers,
            json=json,
            params=params,
        )
        LoggerHelper.log_response(response=response)
        return response

    @classmethod
    @status_code_check
    def head(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "co_python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(
            method="head", url=url, data=data, headers=headers, json=json, params=params
        )
        response = cls.session.request(
            method="head",
            url=url,
            data=data,
            headers=headers,
            json=json,
            params=params,
        )
        LoggerHelper.log_response(response=response)
        return response

    @classmethod
    @status_code_check
    def put(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "co_python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(
            method="put", url=url, data=data, headers=headers, json=json, params=params
        )
        response = cls.session.request(
            method="put", url=url, data=data, headers=headers, json=json, params=params
        )
        LoggerHelper.log_response(response=response)
        return response

    @classmethod
    @status_code_check
    def delete(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "co_python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(method="delete", url=url, headers=headers, data=data)
        response = cls.session.request(
            method="delete", url=url, headers=headers, data=data
        )
        LoggerHelper.log_response(response=response)
        return response

    @classmethod
    @status_code_check
    def options(
        cls: Type[ApiClient],
        path: str = "",
        url: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        headers = headers | {"User-Agent": "co_python_tests"} if headers else headers
        url = url or cls.url + path
        LoggerHelper.log_request(
            method="options",
            url=url,
            data=data,
            headers=headers,
            json=json,
            params=params,
        )
        response = cls.session.request(
            method="options",
            url=url,
            data=data,
            headers=headers,
            json=json,
            params=params,
        )
        LoggerHelper.log_response(response=response)
        return response
