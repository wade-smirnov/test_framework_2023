import time
from functools import wraps

import requests

from framework.errors import Infrastructure500
from framework.helpers.config_helper import get_config
from framework.utils import LOGGER


def retry_test(total_attempts=2, wait_fixed=1):
    def decorator(test_func_ref):
        @wraps(test_func_ref)
        def wrapper(*args, **kwargs):
            retry_count = 1

            launch = get_config("launch")

            while retry_count < total_attempts:
                try:
                    return test_func_ref(*args, **kwargs)

                except Infrastructure500 as e:
                    if launch == "gitlab":
                        LOGGER.info(
                            f'Retry error: "{test_func_ref.__name__}" --> '
                            f"infrastructure 500 error. {e}"
                            f"[{retry_count}/{total_attempts - 1}] "
                            f"Retrying new execution in {wait_fixed} second(s)"
                        )
                        time.sleep(wait_fixed)
                        retry_count += 1
                    else:
                        raise Infrastructure500(str(e))
                except (AssertionError, ValueError) as e:
                    if launch == "gitlab":
                        if "was not listened in ws" in str(e):
                            LOGGER.info(
                                f'Retry error: "{test_func_ref.__name__}" --> '
                                f"WEBSOCKET ERROR. {e}"
                                f"[{retry_count}/{total_attempts - 1}] "
                                f"Retrying new execution in {wait_fixed} second(s)"
                            )
                            time.sleep(wait_fixed)
                            retry_count += 1
                        else:
                            raise ValueError(str(e))
                    else:
                        raise ValueError(str(e))

                except requests.exceptions.ConnectionError as e:
                    if launch == "gitlab":
                        LOGGER.info(
                            f'Retry error: "{test_func_ref.__name__}" --> '
                            f"Connection is missed. {e}"
                            f"[{retry_count}/{total_attempts - 1}] "
                            f"Retrying new execution in {wait_fixed} second(s)"
                        )
                        time.sleep(wait_fixed)
                        retry_count += 1
                    else:
                        raise requests.exceptions.ConnectionError(str(e))

                except Exception as e:  # noqa
                    raise Exception(str(e))

            return test_func_ref(*args, **kwargs)

        return wrapper

    return decorator
