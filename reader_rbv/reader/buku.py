import logging

from bs4 import BeautifulSoup, Tag
from requests import Session
from typing import Any, Dict, Optional, Mapping

from . import Modul
from .utils import get_url


def parse_doc(href: str) -> str:
    # index.php?subfolder=MSIM4103/&doc=DAFIS.pdf
    return href.split("=")[-1]


class Buku(Mapping[str, Modul]):
    def __init__(
        self,
        kode: str,
        base: str,
        session: Session,
        username: str,
        password: str,
        moduls: Optional[Dict[str, Modul]] = None,
    ):
        self.logger = logging.getLogger(f"Buku:{kode}")
        self.kode = kode
        self.base = base
        self.session = session
        self.username = username
        self.password = password
        if moduls:
            self.moduls = moduls
        else:
            self.moduls = dict()
        if not self.moduls:
            self.fetch()

    def __getitem__(self, key: str):
        return self.moduls[key]

    def __iter__(self):
        return iter(self.moduls)

    def __len__(self):
        return len(self.moduls)

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
        for th in soup.findAll("th"):
            a: Tag = th.find("a")
            if not a:
                continue
            url = a["href"]
            doc = parse_doc(url)
            modul = Modul(
                nama=a.getText(),
                subfolder=self.kode,
                doc=doc,
                base=self.base,
                url=url,
                username=self.username,
                password=self.password,
                session=self.session,
            )
            self.moduls[modul.doc] = modul
            self.logger.debug(f"Dapat submodul {doc}")

    def asdict(self) -> Dict[str, Any]:
        return {
            "kode": self.kode,
            "moduls": [modul.asdict() for key, modul in self.moduls.items()],
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        base: str,
        session: Session,
        username: str,
        password: str,
    ):
        moduls: Dict[str, Modul] = dict()
        for md in data["moduls"]:
            moduls[md["doc"]] = Modul.from_dict(
                data=md,
                base=base,
                username=username,
                password=password,
                session=session,
            )
        return cls(
            kode=data["kode"],
            base=base,
            session=session,
            username=username,
            password=password,
            moduls=moduls,
        )
