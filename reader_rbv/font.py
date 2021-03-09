import attr


@attr.dataclass(slots=True)
class Font:
    fontspec: str
    size: str
    family: str
    color: str
