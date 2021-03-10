import attr
import os
import ujson as json
from typing import List, Optional, TYPE_CHECKING

from . import Font, Text
from .utils import get_default_dir, make_dir

if TYPE_CHECKING:
    from . import BookSection


@attr.dataclass(slots=True)
class Page:
    number: int
    pages: int
    height: int
    width: int
    fonts: List[Font] = attr.ib(factory=list)
    text: List[Text] = attr.ib(factory=list, converter=Text.from_list)  # type: ignore
    texts: Optional[str] = None

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

    @classmethod
    def from_cache(cls, section: "BookSection", page: int) -> Optional["Page"]:
        filepath = cls._filepath(section.subfolder, section.doc, page, create=False)
        if not os.path.isfile(filepath):
            return None
        with open(filepath, "r") as fp:
            json_dict = json.load(fp)
        return cls(**json_dict)

    def __str__(self) -> str:
        if self.texts is not None:
            return self.texts
        elif not self.text:
            return ""
        now = 0
        out = ""
        for text in sorted(self.text):
            if text.height != now:
                out += "\n"
                now = text.height
            out += str(text)
        self.texts = out
        return out

    @staticmethod
    def _filepath(code: str, doc: str, page: int, create: bool = True) -> str:
        selection_path = os.path.join(get_default_dir(), code)
        if create:
            make_dir(selection_path)
        return os.path.join(selection_path, f"{doc}-{page}.json")

    def save_to_file(self, code: str, doc: str):
        filepath = self._filepath(code, doc, self.number)
        if os.path.isfile(filepath):
            return
        json_data = attr.asdict(self)
        with open(filepath, "w") as fp:
            json.dump(json_data, fp)
