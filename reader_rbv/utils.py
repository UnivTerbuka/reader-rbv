import logging
import os

from bs4 import BeautifulSoup, Tag
from pathlib import Path
from requests import Response, Session
from typing import Dict, Optional, Type, Union, TYPE_CHECKING

from reader_rbv.exception import InvalidCredential, Unreachable, BookNotFound

if TYPE_CHECKING:
    from . import BookSection

logger = logging.getLogger(__name__)


def clean_doc(doc: str, rstrip: str = ".pdf") -> str:
    # DAFIS.pdf -> DAFIS
    return doc.rstrip(rstrip)


def parse_doc(href: str, strip: str = ".pdf") -> str:
    # index.php?subfolder=MSIM4103/&doc=DAFIS.pdf -> DAFIS
    return href.split("=")[-1].strip(strip)


def sections_from_json(
    sections: Dict[str, Dict],
    m: Type["BookSection"],
    base: str,
    username: str,
    password: str,
    session: Session,
) -> Dict[str, "BookSection"]:
    results: Dict[str, "BookSection"] = dict()
    for key, modul in sections.items():
        results[key] = m.from_dict(
            data=modul,
            base=base,
            username=username,
            password=password,
            session=session,
        )
    return results


def sections_to_json(sections: Dict[str, "BookSection"]) -> Dict[str, Dict]:
    results: Dict[str, Dict] = dict()
    for key, modul in sections.items():
        results[key] = modul.asdict()
    return results


def get_default_dir() -> str:
    # Thank you pre-commit
    ret = os.environ.get("READER_RBV_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"),
        "reader-rbv",
    )
    return os.path.realpath(ret)


def make_dir(path: str):
    if os.path.isdir(path):
        return
    Path(path).mkdir(parents=True, exist_ok=True)


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
    *args,
    **kwargs,
) -> Response:
    res = session.get(url, params=params, headers=headers, *args, **kwargs)
    if not res.ok:
        raise Unreachable("RBV tidak dapat dihubungi")
    elif not res.text:
        raise BookNotFound("Book / halaman tidak ditemukan di RBV")
    elif "About RBV V.2" not in res.text:
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
