import os

from pytest import fixture
from dotenv import load_dotenv

from reader_rbv import Reader, BukuCache

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
def reader(username: str, password: str, base_url: str) -> Reader:
    return Reader(
        username=username,
        password=password,
        cache=BukuCache(0, 600),
        base=base_url,
    )
