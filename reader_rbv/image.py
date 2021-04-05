import attr
import logging
import os
from requests import Session
from typing import Optional
from urllib.parse import urlencode

from .utils import get_default_dir, get_url

logger = logging.getLogger(__name__)


@attr.dataclass(slots=True)
class Image:
    doc: str
    subfolder: str
    page: int
    base: str
    filepath: Optional[str] = None

    def download(self, session: Session, username: str, password: str) -> str:
        if self.is_exist() and self.filepath:
            logger.debug(f"Exist {self.filepath}!")
            return self.filepath
        url = self.url
        res = get_url(
            session=session,
            url=url,
            username=username,
            password=password,
            headers=self._headers,
            stream=True,
        )
        filepath = self._filepath
        with open(filepath, "wb") as fp:
            for chunk in res.iter_content(1024):
                fp.write(chunk)
        self.filepath = filepath
        return filepath

    @property
    def url(self) -> str:
        return self.base + "services/view.php?" + urlencode(self._query)

    def is_exist(self, filepath: Optional[str] = None) -> bool:
        filepath = filepath or self.filepath
        if filepath:
            return os.path.isfile(filepath)
        return False

    @property
    def _filepath(self) -> str:
        base = get_default_dir()
        return os.path.join(base, self.subfolder, f"{self.doc}-{self.page}.jpg")

    @property
    def _headers(self) -> dict:
        return {"Referer": self.base + f"index.php?modul={self.doc}"}

    @property
    def _query(self) -> dict:
        return {
            "doc": self.doc,
            "format": "jpg",
            "subfolder": self.subfolder,
            "page": self.page,
        }
