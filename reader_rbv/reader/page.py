import attr
import ujson as json
from typing import List

from . import Font, Text


@attr.dataclass(slots=True)
class Page:
    number: int
    pages: int
    height: int
    width: int
    fonts: List[Font] = attr.field(factory=list)
    text: List[Text] = attr.field(factory=list, converter=Text.from_list)  # type: ignore

    @classmethod
    def from_jsonp(cls, jsonp: str) -> List["Page"]:
        pages_data = json.loads(jsonp)
        results: List["Page"] = list()
        for page_data in pages_data:
            results.append(
                Page(
                    number=page_data["number"],
                    pages=page_data["pages"],
                    height=page_data["height"],
                    width=page_data["width"],
                    fonts=page_data["fonts"],
                    text=page_data["text"],
                )
            )
        return results
