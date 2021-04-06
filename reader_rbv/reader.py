import logging
import warnings

from cachetools import cachedmethod
from operator import attrgetter
from requests import Session
from typing import Mapping, MutableMapping, Optional

from reader_rbv.exception import BookNotFound, Unreachable
from . import Book, BookCache
from .constants import HEADERS


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

    def get_buku(self, code: str) -> Book:
        warnings.warn(
            "Deprecated Reader.get_buku in favour of Reader.get_book",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_book(code)

    @cachedmethod(attrgetter("cache"))
    def get_book(self, code: str) -> Book:
        if self.cache is not None:
            cached_book = Book.from_cache(
                code=code,
                username=self.username,
                password=self.password,
                base=self.base,
                session=self.session,
            )
            if cached_book is not None:
                return cached_book
        params = {"modul": code}
        self.logger.debug(f"Finding book with code = {code}")
        res = self.session.get(self.base, params=params)
        if not res.ok:
            raise Unreachable("Server unreachable")
        elif not res.text:
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

    def __del__(self):
        if self.cache:
            while self.cache:
                self.cache.popitem()

    def __getitem__(self, key: str) -> Book:
        return self.get_book(key)

    def __len__(self):
        return len(self.cache)

    def __iter__(self):
        return iter(self.cache)
