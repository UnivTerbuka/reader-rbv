import attr
from typing import List, Union


@attr.dataclass(slots=True)
class Text:
    height: int = attr.ib(order=True)
    hLines: int = attr.ib(order=True)
    vline: int = attr.ib(order=False)
    fills: int = attr.ib(order=False)
    font: int = attr.ib(order=False)
    text: str = attr.ib(order=False)

    @classmethod
    def from_data(cls, data: Union[dict, list]) -> "Text":
        if isinstance(data, list):
            return cls(*data)
        return cls(**data)

    @classmethod
    def from_list(cls, data: List[list]) -> List["Text"]:
        results: List["Text"] = list()
        for dat in data:
            results.append(cls.from_data(dat))
        return results

    def __str__(self):
        return self.text
