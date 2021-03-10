import logging

from cachetools import cachedmethod
from operator import attrgetter
from requests import Session
from typing import Mapping, MutableMapping, Optional

from reader_rbv.exception import BookNotFound
from . import Book, BookCache
from .constants import HEADERS
from .utils import get_cached_buku


class Reader(Mapping[str, Book]):
    def __init__(
        self,
        username: str,
        password: str,
        cache: Optional[MutableMapping[str, Book]] = BookCache(10, 600),
        base: str = "http://www.pustaka.ut.ac.id/reader/",
        session: Session = Session(),
    ):
        self.username = username
        self.password = password
        self.session = session
        self.base = base
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.cache = cache
        if cache is None:
            self.logger.debug(".cache disabled")
        self.session.headers.update(HEADERS)

    @cachedmethod(attrgetter("cache"))
    def get_buku(self, code: str) -> Book:
        buku_data = get_cached_buku(code)
        if self.cache is not None and buku_data:
            return Book.from_dict(
                data=buku_data,
                base=self.base,
                session=self.session,
                username=self.username,
                password=self.password,
            )
        params = {"modul": code}
        self.logger.debug(f"Finding book with code = {code}")
        res = self.session.get(self.base, params=params)
        if not res.ok or not res.text:
            raise BookNotFound(f"Unable to find book with code = {code}")
        else:
            self.logger.debug(f"Found book with code = {code}")
        return Book(
            code=code,
            base=self.base,
            session=self.session,
            username=self.username,
            password=self.password,
        )

    def __getitem__(self, key: str) -> Book:
        return self.get_buku(key)

    def __len__(self):
        return len(self.cache)

    def __iter__(self):
        return iter(self.cache)
