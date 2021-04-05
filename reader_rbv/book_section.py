from cachetools import cachedmethod, LRUCache
from operator import attrgetter
from requests import Session
from typing import Any, Dict, List, Mapping, MutableMapping, Optional
from urllib.parse import urlencode

from . import Image, Page, PageCache
from .utils import get_url, clean_doc


class BookSection(Mapping[int, Page]):
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
        self.page_cache: MutableMapping[int, Page] = PageCache(
            code=subfolder,
            doc=doc,
            maxsize=50,
            ttl=600,
        )
        self.image_cache: MutableMapping[int, Image] = LRUCache(50)
        self.__username__ = username
        self.__password__ = password
        self._max_page = 0
        if max_page is None:
            self._max_page = self.get_max_page()
        else:
            self._max_page = max_page

    def __del__(self):
        while self.page_cache:
            self.page_cache.popitem()

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
    def max_page(self) -> int:
        return self._max_page

    def get_max_page(self) -> int:
        page1 = self.get_page(1)
        return page1.pages

    def add_cache_pages(self, pages: List[Page]):
        for page in pages:
            self.page_cache[page.number] = page

    @cachedmethod(attrgetter("page_cache"))
    def get_page(self, page: int) -> Page:
        if page < 1:
            raise KeyError("key must be greater than 0")
        elif self.max_page and page > self.max_page:
            raise KeyError("key cant be greater than max_page")
        cached_page = Page.from_cache(self, page=page)
        if cached_page:
            return cached_page
        res = get_url(
            session=self.session,
            url=self.base + "services/view.php",
            params=self._params(page),
            username=self.__username__,
            password=self.__password__,
            headers=self._headers,
        )
        jsonp = res.text[1:-1]
        pages = Page.from_jsonp(jsonp)
        self.add_cache_pages(pages)
        return self.page_cache[page]

    @cachedmethod(attrgetter("image_cache"))
    def get_image(self, page: int) -> Image:
        image = Image(doc=self.doc, subfolder=self.subfolder, page=page, base=self.base)
        if not image.is_exist():
            image.download(
                session=self.session,
                username=self.__username__,
                password=self.__password__,
            )
        return image

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        base: str,
        username: str,
        password: str,
        session: Session,
    ) -> "BookSection":
        return cls(
            base=base,
            username=username,
            password=password,
            session=session,
            **data,
        )

    @property
    def _headers(self) -> dict:
        return {"Referer": self.base + "?" + urlencode({"modul": self.subfolder})}

    def _params(self, page: int, format_: str = "jsonp") -> dict:
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
