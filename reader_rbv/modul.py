from cachetools import cachedmethod
from operator import attrgetter
from requests import Session
from typing import Any, Dict, List, Mapping, MutableMapping, Optional
from urllib.parse import urlencode

from . import Page, PageCache
from .utils import get_url, get_cached_page, clean_doc


class Modul(Mapping[int, Page]):
    def __init__(
        self,
        nama: str,
        subfolder: str,
        doc: str,
        base: str,
        url: str,
        username: str,
        password: str,
        session: Session,
        max_page: Optional[int] = None,
    ):
        self.nama = nama
        self.subfolder = subfolder
        self.doc = clean_doc(doc)
        self.base = base
        self.url = url
        self.session = session
        self.cache: MutableMapping[int, Page] = PageCache(
            kode=subfolder,
            doc=doc,
            maxsize=50,
            ttl=600,
        )
        self._max_page = max_page
        self.__username__ = username
        self.__password__ = password
        if self.max_page is None:
            self.fetch()

    def __str__(self):
        return self.nama

    def __getitem__(self, key: int) -> Page:
        return self.get_page(key)

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
        if not isinstance(value, int):
            raise ValueError("max_page harus int")
        self._max_page = value

    def fetch(self) -> None:
        page1 = self.get_page(1)
        self.max_page = page1.pages

    def add_cache(self, pages: List[Page]):
        for page in pages:
            self.cache[page.number] = page

    @cachedmethod(attrgetter("cache"))
    def get_page(self, page: int) -> Page:
        if page < 1:
            raise KeyError("key harus > 0")
        elif self.max_page and page > self.max_page:
            raise KeyError("key melebihi halaman maksimal")
        page_data = get_cached_page(self.subfolder, self.doc, page)
        if page_data:
            return Page(**page_data)  # type: ignore[call-arg]
        params = self.__make_params__(page)
        headers = {"Referer": self.base + "?" + urlencode({"modul": self.subfolder})}
        res = get_url(
            session=self.session,
            url=self.base + "services/view.php",
            params=params,
            username=self.__username__,
            password=self.__password__,
            headers=headers,
        )
        jsonp = res.text[1:-1]
        pages = Page.from_jsonp(jsonp)
        self.add_cache(pages)
        return self.cache[page]

    def __make_params__(self, page: int, format_: str = "jsonp") -> dict:
        return {
            "doc": self.doc,
            "format": format_,
            "subfolder": self.subfolder + "/",
            "page": (page // 10 + 1) * 10,
        }

    def asdict(self) -> Dict[str, Any]:
        return {
            "nama": self.nama,
            "subfolder": self.subfolder,
            "doc": self.doc,
            "max_page": self.max_page,
            "url": self.url,
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        base: str,
        username: str,
        password: str,
        session: Session,
    ) -> "Modul":
        return cls(
            base=base,
            username=username,
            password=password,
            session=session,
            **data,
        )
