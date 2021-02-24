import attr
from typing import List

from . import Font


@attr.dataclass(slots=True)
class Page:
    number: int
    pages: int
    height: int
    width: int
    fonts: List[Font] = attr.field(factory=list)
    text: List[list] = attr.field(factory=list)
