from cachetools import Cache, LRUCache, cachedmethod
from operator import attrgetter
from requests import Session
from typing import Optional, Mapping

from . import Page


class Modul(Mapping[int, Page]):
    def __init__(
        self,
        subfolder: str,
        doc: str,
        base: str,
        session: Session,
        cache: Cache[int, Page] = LRUCache(100),
        max_page: Optional[int] = None,
    ):
        self.subfolder = subfolder
        self.base = base
        self.session = Session
        self.cache = cache
        self._max_page = max_page
        if not self.max_page:
            self.fetch()

    def __iter__(self):
        self.__current__ = 1
        return self

    def __next__(self):
        if self.__current__ <= self.max_page:
            result = self.get_page(self.__current__)
            self.__current__ += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        return self.max_page

    @property
    def max_page(self) -> Optional[int]:
        return self._max_page

    @max_page.setter
    def max_page(self, value: int):
        if isinstance(value, int):
            self._max_page = value
        raise ValueError("max_page harus int")

    def fetch(self) -> None:
        pass

    @attrgetter("cache")
    def get_page(self, page: int) -> Page:
        pass
