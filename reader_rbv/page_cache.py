import time
from cachetools import TTLCache


class PageCache(TTLCache):
    def __init__(
        self,
        code: str,
        doc: str,
        maxsize: int,
        ttl: int,
        timer=time.monotonic,
        getsizeof=None,
    ):
        self.code = code
        self.doc = doc
        super().__init__(maxsize, ttl, timer=timer, getsizeof=getsizeof)

    def popitem(self):
        key, value = super().popitem()
        value.save_to_file(self.code, self.doc)
        return key, value
