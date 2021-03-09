import logging

from cachetools import cachedmethod
from operator import attrgetter
from requests import Session
from typing import MutableMapping

from reader_rbv.exception import BookNotFound
from . import Buku, BukuCache
from .constants import HEADERS
from .utils import get_cached_buku


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
        self.cache: MutableMapping[str, Buku] = BukuCache(10, 600)
        self.logger = logging.getLogger(f"Reader:{username}")
        self.session.headers.update(HEADERS)

    @cachedmethod(attrgetter("cache"))
    def get(self, kode: str) -> Buku:
        buku_data = get_cached_buku(kode)
        if buku_data:
            return Buku.from_dict(
                data=buku_data,
                base=self.base,
                session=self.session,
                username=self.username,
                password=self.password,
            )
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
