from bs4 import BeautifulSoup, Tag
from requests import Response, Session
from typing import Union

from reader_rbv.exception import InvalidCredential, Unreachable


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
    params: dict,
    username: str,
    password: str,
) -> Response:
    res = session.get(url, params=params)
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
    res = session.post(url, params=params)
    if not res.ok:
        raise InvalidCredential("Username / password salah")
    return res