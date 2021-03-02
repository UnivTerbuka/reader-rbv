import time
from cachetools import TTLCache

from .utils import cache_page


class PageCache(TTLCache):
    def __init__(
        self,
        kode: str,
        doc: str,
        maxsize: int,
        ttl: int,
        timer=time.monotonic,
        getsizeof=None,
    ):
        self.kode = kode
        self.doc = doc
        super().__init__(maxsize, ttl, timer=timer, getsizeof=getsizeof)

    def popitem(self):
        key, value = super().popitem()
        cache_page(value, self.kode, self.doc)
        return key, value
