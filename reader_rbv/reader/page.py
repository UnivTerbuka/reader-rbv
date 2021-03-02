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
    fonts: List[Font] = attr.ib(factory=list)
    text: List[Text] = attr.ib(factory=list, converter=Text.from_list)  # type: ignore
    texts: str = ""

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

    def __str__(self) -> str:
        if self.texts:
            return self.texts
        elif not self.text:
            return "Halaman kosong / Tidak ditemukan. :("
        now = 0
        out = ""
        for text in sorted(self.text):
            if text.height != now:
                out += "\n"
                now = text.height
            out += str(text)
        self.texts = out
        return out
