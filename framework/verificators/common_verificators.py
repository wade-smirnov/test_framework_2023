import functools
import requests
from framework.errors import Infrastructure500


def status_code_check(func: callable) -> callable:
    @functools.wraps(func)
    def function(*args, **kwargs) -> requests.Response:
        expected_status_code = kwargs.pop("status_code")
        returned_value = func(*args, **kwargs)
        error_message = (
            f"\nerror message: {returned_value.text}"
            if returned_value.text
            else "\nNo error Message"
        )
        if isinstance(expected_status_code, int):
            if (
                returned_value.status_code != expected_status_code
            ) and returned_value.status_code == 500:
                raise Infrastructure500("Infrastructure is not ok")
            else:
                assert expected_status_code == returned_value.status_code, (
                    f"\n\nReturned status code {returned_value.status_code} "
                    f"does not match expected {expected_status_code}" + error_message
                )
        elif isinstance(expected_status_code, tuple):
            if (
                returned_value.status_code not in expected_status_code
            ) and returned_value.status_code == 500:
                raise Infrastructure500("Infrastructure is not ok")
            else:
                assert returned_value.status_code in expected_status_code, (
                    f"\n\nReturned status code {returned_value.status_code} "
                    f"does not match expected {expected_status_code}, " + error_message
                )
        return returned_value

    return function


def check_response_has_no_header(response: requests.Response, header: str):
    assert (
        header not in response.headers
    ), f"Header {header} must be absent in response headers"
