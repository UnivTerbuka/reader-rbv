import attr
import logging

from bs4 import BeautifulSoup, Tag
from requests import Session
from typing import Any, Dict, Mapping

from . import BookSection
from .utils import get_url, parse_doc, sections_to_json, sections_from_json


logger = logging.getLogger(__name__)


@attr.dataclass(slots=True)
class Book(Mapping[str, BookSection]):
    code: str
    base: str
    username: str
    password: str
    session: Session = attr.ib(factory=Session)
    sections: Dict[str, BookSection] = attr.ib(factory=dict)

    def __attrs_post_init__(self) -> None:
        if not self.sections:
            logger.debug(f"{self.code} Section is empty, gettig from the server")
            self.fetch()

    def __getitem__(self, key: str):
        logger.debug(f"{self.code} Getting section {key}")
        return self.sections[key]

    def __iter__(self):
        return iter(self.sections)

    def __len__(self):
        return len(self.sections)

    def fetch(self):
        params = {"modul": self.code}
        res = get_url(
            session=self.session,
            url=self.base,
            params=params,
            username=self.username,
            password=self.password,
        )
        logger.debug(f"{self.code} Getting all sections")
        soup = BeautifulSoup(res.text, "html.parser")
        for th in soup.findAll("th"):
            a: Tag = th.find("a")
            if not a:
                continue
            url = a["href"]
            doc = parse_doc(url)
            modul = BookSection(
                nama=a.getText(),
                subfolder=self.code,
                doc=doc,
                base=self.base,
                url=url,
                username=self.username,
                password=self.password,
                session=self.session,
            )
            self.sections[modul.doc] = modul
            logger.debug(f"{self.code} Got section {modul}")
        logger.debug(f"{self.code} Successfully fetch {len(self.sections)} sections")

    def asdict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
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
            code=data["code"],
            base=base,
            session=session,
            username=username,
            password=password,
            sections=sections,
        )
