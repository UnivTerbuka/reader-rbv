import logging

from cachetools import Cache, TTLCache, cachedmethod
from operator import attrgetter
from requests import Session
from typing import List

from reader_rbv.exception import ModulNotFound
from . import Modul


class Buku:
    def __init__(
        self,
        kode: str,
        base: str,
        session: Session,
        cache: Cache[str, Modul] = TTLCache[str, Modul](10, 1800),
    ):
        self.kode = kode
        self.base = base
        self.session = session
        self.cache = cache
        self.moduls: List[str] = list()
        self.logger = logging.getLogger(f"Buku:{kode}")

    @cachedmethod(attrgetter("cache"))
    def get(self, doc: str):
        if doc not in self.moduls:
            self.logger.warning(f"Submodul {doc} tidak ada")
            raise ModulNotFound(f"Modul {doc} tidak ada di buku {self.kode}")
        else:
            self.logger.debug(f"Submodul {doc} ditemukan")
        return Modul(self.kode, doc, self.base, self.session)
