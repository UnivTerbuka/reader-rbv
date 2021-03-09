import os

from pytest import fixture
from dotenv import load_dotenv

from reader_rbv import Reader

load_dotenv()


@fixture
def username(self) -> str:
    return os.environ.get("USERNAME_RBV", "")


@fixture
def password(self) -> str:
    return os.environ.get("PASSWORD_RBV", "")


@fixture
def reader(self, username: str, password: str) -> Reader:
    return Reader(username, password)
