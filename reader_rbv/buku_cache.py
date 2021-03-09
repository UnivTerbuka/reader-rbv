import time
from cachetools import TTLCache

from .utils import cache_buku


class BukuCache(TTLCache):
    def __init__(self, maxsize, ttl, timer=time.monotonic, getsizeof=None):
        super().__init__(maxsize, ttl, timer=timer, getsizeof=getsizeof)

    def popitem(self):
        key, value = super().popitem()
        cache_buku(value)
        return key, value
