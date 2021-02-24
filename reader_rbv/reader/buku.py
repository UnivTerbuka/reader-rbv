import logging

from bs4 import BeautifulSoup, Tag
from cachetools import Cache, TTLCache, cachedmethod
from operator import attrgetter
from requests import Session
from typing import List, Optional

from reader_rbv.exception import ModulNotFound
from . import Modul
from .utils import get_url


def parse_doc(href: str) -> str:
    # index.php?subfolder=MSIM4103/&doc=DAFIS.pdf
    return href.split("=")[-1]


class Buku:
    def __init__(
        self,
        kode: str,
        base: str,
        session: Session,
        username: str,
        password: str,
        cache: Cache[str, Modul] = TTLCache[str, Modul](10, 1800),
        moduls: Optional[List[str]] = None,
    ):
        self.kode = kode
        self.base = base
        self.session = session
        self.username = username
        self.password = password
        self.cache = cache
        if moduls:
            self.moduls = moduls
        else:
            self.moduls = list()
        if not self.moduls:
            self.fetch()
        self.logger = logging.getLogger(f"Buku:{kode}")

    @cachedmethod(attrgetter("cache"))
    def get(self, doc: str):
        # DAFIS.pdf
        if doc not in self.moduls:
            self.logger.warning(f"Submodul {doc} tidak ada")
            raise ModulNotFound(f"Modul {doc} tidak ada di buku {self.kode}")
        else:
            self.logger.debug(f"Submodul {doc} ditemukan")
        return Modul(self.kode, doc, self.base, self.session)

    def fetch(self):
        params = {"modul": self.kode}
        res = get_url(
            session=self.session,
            url=self.base,
            params=params,
            username=self.username,
            password=self.password,
        )
        self.logger.debug("Mencari submodul")
        soup = BeautifulSoup(res.text, "html.parser")
        ths: List[Tag] = soup.findAll("th")
        for th in ths:
            a: Tag = th.find("a")
            if not a:
                continue
            doc = parse_doc(a["href"])
            self.logger.debug(f"Dapat submodul {doc}")
            self.moduls.append(doc)
