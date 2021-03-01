import logging

from cachetools import TTLCache, cachedmethod
from operator import attrgetter
from requests import Session
from typing import MutableMapping

from reader_rbv.exception import BookNotFound
from . import Buku

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
}


class Reader:
    def __init__(
        self,
        username: str,
        password: str,
        base: str = "http://www.pustaka.ut.ac.id/reader/",
        session: Session = Session(),
    ):
        self.username = username
        self.password = password
        self.session = session
        self.base = base
        self.cache: MutableMapping[str, Buku] = TTLCache(10, 600)
        self.logger = logging.getLogger(f"Reader:{username}")
        self.session.headers.update(HEADERS)

    @cachedmethod(attrgetter("cache"))
    def get(self, kode: str) -> Buku:
        params = {"modul": kode}
        self.logger.debug(f"Mencari ketersediaan buku {kode}")
        res = self.session.get(self.base, params=params)
        if not res.ok or not res.text:
            self.logger.warning(f"Buku {kode} tidak ditemukan")
            raise BookNotFound(f"Buku dengan kode {kode} tidak ditemukan")
        else:
            self.logger.debug(f"Buku {kode} ditemukan")
        return Buku(
            kode=kode,
            base=self.base,
            session=self.session,
            username=self.username,
            password=self.password,
        )
