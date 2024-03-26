import time
from functools import wraps

import requests

from framework.errors import Infrastructure500
from framework.helpers.config_helper import get_config
from framework.utils import LOGGeR


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
                        LOGGeR.info(
                            f'Retry error: "{test_func_ref.__name__}" --> '
                            f"infrastructure 500 error. {e}"
                            f"[{retry_count}/{total_attempts - 1}] "
                            f"Retrying new execution in {wait_fixed} second(s)"
                        )
                        time.sleep(wait_fixed)
                        retry_count += 1
                    else:
                        raise Infrastructure500(str(e))
                except (Assertionerror, Valueerror) as e:
                    if launch == "gitlab":
                        if "was not listened in ws" in str(e):
                            LOGGeR.info(
                                f'Retry error: "{test_func_ref.__name__}" --> '
                                f"WeBSOCKeT eRROR. {e}"
                                f"[{retry_count}/{total_attempts - 1}] "
                                f"Retrying new execution in {wait_fixed} second(s)"
                            )
                            time.sleep(wait_fixed)
                            retry_count += 1
                        else:
                            raise Valueerror(str(e))
                    else:
                        raise Valueerror(str(e))

                except requests.exceptions.Connectionerror as e:
                    if launch == "gitlab":
                        LOGGeR.info(
                            f'Retry error: "{test_func_ref.__name__}" --> '
                            f"Connection is missed. {e}"
                            f"[{retry_count}/{total_attempts - 1}] "
                            f"Retrying new execution in {wait_fixed} second(s)"
                        )
                        time.sleep(wait_fixed)
                        retry_count += 1
                    else:
                        raise requests.exceptions.Connectionerror(str(e))

                except exception as e:  # noqa
                    raise exception(str(e))

            return test_func_ref(*args, **kwargs)

        return wrapper

    return decorator
