import logging

from bs4 import BeautifulSoup
from operator import attrgetter
from requests import Session
from cachetools import TTLCache, Cache, cachedmethod

from reader_rbv.exception import InvalidCredential, Unreachable, NotFound
from . import Buku
from .utils import get_captcha


class Reader:
    def __init__(
        self,
        kode: str,
        username: str,
        password: str,
        base: str = "http://www.pustaka.ut.ac.id/reader/",
        session: Session = Session(),
        cache: Cache[str, Buku] = TTLCache[str, Buku](10, 600),
    ):
        self.kode = kode
        self.username = username
        self.password = password
        self.session = session
        self.base = base
        self.cache = cache
        self.logger = logging.getLogger(f"Reader:{kode}")

    @cachedmethod(attrgetter("cache"))
    def get(self, kode: str) -> Buku:
        params = {"modul": kode}
        res = self.session.get(self.base, params=params)
        if not res.ok or not res.text:
            raise NotFound(f"Buku dengan kode {kode} tidak ditemukan")
        return Buku(kode, self.base, self.session)
