import attr
from typing import List


@attr.dataclass(slots=True)
class Text:
    height: int = attr.ib(order=True)
    hLines: int = attr.ib(order=True)
    vline: int = attr.ib(order=False)
    fills: int = attr.ib(order=False)
    font: int = attr.ib(order=False)
    text: str = attr.ib(order=False)

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
