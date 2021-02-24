from cachetools import Cache, LRUCache, cachedmethod
from operator import attrgetter
from requests import Session

from . import Page


class Modul:
    def __init__(self, modul: str, session: Session):
        self.modul = modul
        self.session = Session
        self.cache: Cache[int, Page] = LRUCache(100)

    @cachedmethod(attrgetter("cache"))
    def get(self, page: int):
        pass
