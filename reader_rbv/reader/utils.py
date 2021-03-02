import attr
import logging
import os
import ujson as json

from bs4 import BeautifulSoup, Tag
from pathlib import Path
from requests import Response, Session
from typing import Dict, Optional, Union, TYPE_CHECKING

from reader_rbv.exception import InvalidCredential, Unreachable

if TYPE_CHECKING:
    from . import Buku
    from . import Page

logger = logging.getLogger(__name__)


def get_default_dir() -> str:
    # Thank you pre-commit
    ret = os.environ.get("READER_RBV_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"),
        "reader-rbv",
    )
    return os.path.realpath(ret)


DEFAULT_DIR = get_default_dir()


def get_captcha(form: Tag) -> str:
    c: Union[str, int, float] = ""
    ccaptcha: Tag = form.find("input", {"name": "ccaptcha"})
    q: str = ccaptcha.previous.strip().lower().split()
    # 'Berapa hasil dari 3 + 9 ='
    a = q[3]
    n = q[4]
    b = q[5]
    if n == "+":
        c = int(a) + int(b)
    elif n == "-":
        c = int(a) - int(b)
    elif n == "/" or n == ":":
        c = int(a) / int(b)
    elif n == "*" or n == "x":
        c = int(a) * int(b)
    return str(c)


def get_url(
    session: Session,
    url: str,
    username: str,
    password: str,
    params: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Response:
    res = session.get(url, params=params, headers=headers)
    if not res.ok:
        raise Unreachable("RBV tidak dapat dihubungi")
    elif "Login" not in res.text:
        return res
    soup = BeautifulSoup(res.text, "html.parser")
    data = {
        "_submit_check": "1",
        "username": username,
        "password": password,
        "ccaptcha": get_captcha(soup),
        "submit": "Submit",
    }
    headers = {"Referer": res.url}
    res = session.post(url, data=data, params=params, headers=headers)
    if not res.ok:
        raise InvalidCredential("Username / password salah")
    return res


def cache_page_filepath(kode: str, doc: str, page: int) -> str:
    base_folder = os.path.join(DEFAULT_DIR, kode)
    Path(base_folder).mkdir(parents=True, exist_ok=True)
    return os.path.join(base_folder, f"{doc}-{page}.json")


def cache_buku_filepath(kode: str, ext: str = ".json") -> str:
    return os.path.join(DEFAULT_DIR, kode + ext)


def cache_page(page: "Page", kode: str, doc: str):
    filepath = cache_page_filepath(kode, doc, page.number)
    if os.path.isfile(filepath):
        logger.debug(f"File cache {filepath} sudah ada, dilewati...")
    else:
        json_data = attr.asdict(page)
        with open(filepath, "w") as fp:
            json.dump(json_data, fp)


def get_cached_page(kode: str, doc: str, page: int) -> Optional[dict]:
    filepath = cache_page_filepath(kode, doc, page)
    if not os.path.isfile(filepath):
        return None
    with open(filepath, "r") as fp:
        json_dict = json.load(fp)
    return json_dict


def cache_buku(buku: "Buku"):
    filepath = cache_buku_filepath(buku.kode)
    if os.path.isfile(filepath):
        logger.debug(f"File cache buku {filepath} sudah ada, dilewati...")
    buku_data = buku.asdict()
    with open(filepath, "w") as fp:
        json.dump(buku_data, fp)


def get_cached_buku(kode: str) -> Optional[dict]:
    filepath = cache_buku_filepath(kode)
    if not os.path.isfile(filepath):
        return None
    with open(filepath, "r") as fp:
        json_dict = json.load(fp)
    return json_dict
