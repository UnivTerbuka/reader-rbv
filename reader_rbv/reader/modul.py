from cachetools import Cache, LRUCache, cachedmethod
from operator import attrgetter
from requests import Session

from . import Page


class Modul:
    def __init__(
        self,
        subfolder: str,
        doc: str,
        base: str,
        session: Session,
        cache: Cache[int, Page] = LRUCache(100),
    ):
        self.subfolder = subfolder
        self.base = base
        self.session = Session
        self.cache = cache

    @cachedmethod(attrgetter("cache"))
    def get(self, page: int):
        pass
