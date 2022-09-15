import os

from dotenv import load_dotenv
from pytest import fixture
from requests import Session

from reader_rbv import Reader

load_dotenv()


@fixture
def username() -> str:
    return os.environ.get("USERNAME_RBV", "")


@fixture
def password() -> str:
    return os.environ.get("PASSWORD_RBV", "")


@fixture
def base_url() -> str:
    return os.environ.get("URL_RBV", "")


@fixture
def verify() -> bool:
    ver = os.environ.get("URL_RBV", "Y")
    return ver == "Y"


@fixture
def reader(username: str, password: str, base_url: str, verify: bool) -> Reader:
    session = Session()
    session.verify = verify
    return Reader(
        username=username,
        password=password,
        cache=None,
        base=base_url,
        session=session,
    )
