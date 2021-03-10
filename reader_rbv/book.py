import logging

from bs4 import BeautifulSoup, Tag
from requests import Session
from typing import Any, Dict, Optional, Mapping

from . import BookSection
from .utils import get_url, parse_doc, sections_to_json, sections_from_json


class Book(Mapping[str, BookSection]):
    def __init__(
        self,
        kode: str,
        base: str,
        session: Session,
        username: str,
        password: str,
        sections: Optional[Dict[str, BookSection]] = None,
    ):
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.kode = kode
        self.base = base
        self.session = session
        self.username = username
        self.password = password
        if sections:
            self.sections = sections
        else:
            self.sections = dict()
        if not self.sections:
            self.logger.debug(f"{self.kode} Section is empty, gettig from the server")
            self.fetch()

    def __getitem__(self, key: str):
        self.logger.debug(f"{self.kode} Getting section {key}")
        return self.sections[key]

    def __iter__(self):
        return iter(self.sections)

    def __len__(self):
        return len(self.sections)

    def fetch(self):
        params = {"modul": self.kode}
        res = get_url(
            session=self.session,
            url=self.base,
            params=params,
            username=self.username,
            password=self.password,
        )
        self.logger.debug(f"{self.kode} Getting all sections")
        soup = BeautifulSoup(res.text, "html.parser")
        for th in soup.findAll("th"):
            a: Tag = th.find("a")
            if not a:
                continue
            url = a["href"]
            doc = parse_doc(url)
            modul = BookSection(
                nama=a.getText(),
                subfolder=self.kode,
                doc=doc,
                base=self.base,
                url=url,
                username=self.username,
                password=self.password,
                session=self.session,
            )
            self.sections[modul.doc] = modul
            self.logger.debug(f"{self.kode} Got section {modul}")
        self.logger.debug(
            f"{self.kode} Successfully fetch {len(self.sections)} sections"
        )

    def asdict(self) -> Dict[str, Any]:
        return {
            "kode": self.kode,
            "sections": sections_to_json(self.sections),
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
        sections = sections_from_json(
            sections=data["sections"],
            m=BookSection,
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
            sections=sections,
        )
