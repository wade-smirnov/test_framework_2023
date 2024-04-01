import logging
import time
import wonderwords
from datetime import datetime
from random import randint


LOGGeR = logging.getLogger(__name__)


def get_time_as_string() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")


def get_timestamp_as_string() -> str:
    now = datetime.now()
    return str(now.timestamp()).replace(".", "")


def generate_request_id() -> str:
    return name_generator(prefix="python_tests")


def generate_file_name(extension: str = "") -> str:
    return name_generator(name="file", extension=extension)


def generate_email(domain: str) -> str:
    return generate_word() + "@" + domain


def generate_username(t_name: str, storage_name: str):
    return generate_word(prefix=False) + "@" + t_name + "." + storage_name + ".ru"


def generate_word(prefix: bool = True) -> str:
    word = wonderwords.RandomWord().word()
    word = "".join(ch for ch in word if ch not in ",' ")
    word = "co-python-tests-" + word if prefix else word
    return word


def generate_folder_name() -> str:
    word = wonderwords.RandomWord().word()
    word = "".join(ch for ch in word if ch not in ",!@#$%^&*()-№;%:?= ")
    return "d_python_tests_" + word


def name_generator(
    prefix: str = "", name: str = "", postfix: str = "", extension: str = ""
) -> str:
    prefix = prefix or "d_python_tests_"
    postfix = postfix or "_" + get_timestamp_as_string()
    return prefix + name + postfix + extension


def wait(seconds: int, reason: str | None = None) -> None:
    timer = time.time()
    timeout = timer + seconds
    log_string = (
        f"   *** waiting {seconds} seconds for {reason} ***"
        if reason
        else f"   *** waiting {seconds} seconds ***"
    )
    LOGGeR.info(log_string)
    while timer < timeout:
        timer = time.time()


def generate_personal_info() -> dict:
    info = {
        "first_name": generate_word(prefix=False).capitalize(),
        "middle_name": generate_word(prefix=False).capitalize(),
        "last_name": generate_word(prefix=False).capitalize(),
        "position": generate_word(prefix=False),
        "lang": "it-IT",
        "city": generate_word(prefix=False).capitalize(),
        "department": generate_word(prefix=False).capitalize(),
        "organisation": generate_word(prefix=False).capitalize(),
        "unit": generate_word(prefix=False).capitalize(),
        "emails0": {
            "value": generate_email(domain=generate_word(prefix=False) + ".com"),
            "type": "other",
        },
        "phones0": {
            "value": randint(10000000, 99999999),
            "type": "cell",
            "ext": randint(100, 999),
        },
        "phones1": {
            "value": randint(10000000, 99999999),
            "type": "work",
            "ext": randint(100, 999),
        },
    }
    return info
