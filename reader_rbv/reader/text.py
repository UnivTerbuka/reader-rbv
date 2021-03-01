import attr
from typing import List


@attr.dataclass(slots=True)
class Text:
    height: int
    hLines: int
    vline: int
    fills: int
    font: int
    text: str

    @classmethod
    def from_data(cls, data: list) -> "Text":
        return cls(
            height=data[0],
            hLines=data[1],
            vline=data[2],
            fills=data[3],
            font=data[4],
            text=data[5],
        )

    @classmethod
    def from_list(cls, data: List[list]) -> List["Text"]:
        results: List["Text"] = list()
        for dat in data:
            results.append(cls.from_data(dat))
        return results

    def __str__(self):
        return self.text
