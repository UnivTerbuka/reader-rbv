from requests import Session
from typing import Dict, Optional

from . import Modul


class Buku:
    def __init__(
        self,
        kode: str,
        base: str,
        session: Session,
        moduls: Optional[Dict[str, Modul]] = None,
    ):
        self.kode = kode
        self.base = base
        self.session = session
        if moduls:
            self._moduls = moduls
        else:
            self._moduls = dict()

    @property
    def moduls(self) -> Dict[str, Modul]:
        return self._moduls

    def fetch(self):
        pass
