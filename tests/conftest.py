import os

from pytest import fixture
from dotenv import load_dotenv

from reader_rbv import Reader

load_dotenv()


@fixture
def username() -> str:
    return os.environ.get("USERNAME_RBV", "")


@fixture
def password() -> str:
    return os.environ.get("PASSWORD_RBV", "")


@fixture
def reader(username: str, password: str) -> Reader:
    return Reader(username, password)
