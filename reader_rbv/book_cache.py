from cachetools import TTLCache

from .utils import cache_buku


class BookCache(TTLCache):
    def popitem(self):
        key, value = super().popitem()
        cache_buku(value)
        return key, value
