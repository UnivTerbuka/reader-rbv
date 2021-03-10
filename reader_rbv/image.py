import attr
from urllib.parse import urlencode


@attr.dataclass(slots=True)
class Image:
    doc: str
    subfolder: str
    page: int
    base: str

    @property
    def url(self) -> str:
        query = {
            "doc": self.doc,
            "format": "jpg",
            "subfolder": self.subfolder,
            "page": self.page,
        }
        return self.base + "services/view.php?" + urlencode(query)
