from cachetools import TTLCache

from .utils import cache_book


class BookCache(TTLCache):
    def popitem(self):
        key, value = super().popitem()
        cache_book(value)
        return key, value
