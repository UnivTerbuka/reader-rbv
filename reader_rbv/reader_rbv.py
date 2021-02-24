from cachetools import Cache, TTLCache, cachedmethod
from operator import attrgetter
from requests import Session

from . import Reader


class ReaderRbv:
    def __init__(
        self,
        username: str,
        password: str,
        cache: Cache[str, Reader] = TTLCache(50, 1800),
    ):
        self.username = username
        self.password = password
        self.session = Session()
        self.cache = cache

    @cachedmethod(attrgetter("cache"))
    def get(self, kode: str):
        pass
