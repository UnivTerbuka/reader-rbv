import logging

from cachetools import Cache, TTLCache, cachedmethod
from operator import attrgetter
from requests import Session

from reader_rbv.exception import BookNotFound
from . import Buku


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
        self.logger.debug(f"Mencari ketersediaan buku {kode}")
        res = self.session.get(self.base, params=params)
        if not res.ok or not res.text:
            self.logger.warning(f"Buku {kode} tidak ditemukan")
            raise BookNotFound(f"Buku dengan kode {kode} tidak ditemukan")
        else:
            self.logger.debug(f"Buku {kode} ditemukan")
        return Buku(kode, self.base, self.session)
