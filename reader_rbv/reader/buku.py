from cachetools import Cache, TTLCache, cachedmethod
from operator import attrgetter
from requests import Session
from typing import Dict, List, Optional

from reader_rbv.exception import ModulNotFound
from . import Modul


class Buku:
    def __init__(
        self,
        kode: str,
        base: str,
        session: Session,
        cache: Cache[str, Modul] = TTLCache[str, Modul](10, 1800),
        moduls: Optional[Dict[str, Modul]] = None,
    ):
        self.kode = kode
        self.base = base
        self.session = session
        self.cache = cache
        if moduls:
            for key, value in moduls.items():
                self.cache[key] = value
        self.moduls: List[str] = list()

    def fetch(self):
        pass

    @cachedmethod(attrgetter("cache"))
    def get(self, doc: str):
        if doc not in self.moduls:
            raise ModulNotFound(f"Modul {doc} tidak ditemukan di buku {self.kode}")
        return Modul(self.kode, doc, self.base, self.session)
