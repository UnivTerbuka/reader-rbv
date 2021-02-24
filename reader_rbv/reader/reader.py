from operator import attrgetter
from requests import Session
from cachetools import TTLCache, Cache, cachedmethod

from . import Modul


class Reader:
    def __init__(
        self,
        kode: str,
        session: Session,
        cache: Cache[str, Modul] = TTLCache[str, Modul](10, 600),
    ):
        self.kode = kode
        self.session = session
        self.cache = cache

    @cachedmethod(attrgetter("cache"))
    def get(self, modul: str) -> Modul:
        return Modul(modul, self.session)
