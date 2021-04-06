import attr
import logging
import os
from requests import Session
from typing import Optional
from urllib.parse import urlencode

from .utils import get_default_dir, get_image, make_dir

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
        return get_image(
            session=session,
            username=username,
            password=password,
            image=self,
        )

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
        subfolder = os.path.join(base, self.subfolder)
        make_dir(subfolder)
        return os.path.join(subfolder, f"{self.doc}-{self.page}.jpg")

    @property
    def _headers(self) -> dict:
        return {"Referer": self.base + f"index.php?modul={self.subfolder}"}

    @property
    def _query(self) -> dict:
        return {
            "doc": self.doc,
            "format": "jpg",
            "subfolder": f"{self.subfolder}/",
            "page": self.page,
        }
