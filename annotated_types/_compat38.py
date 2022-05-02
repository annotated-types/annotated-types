import sys
from typing import TypeVar

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol


T = TypeVar("T")


class SupportsGt(Protocol):
    def __gt__(self: T, other: T, /) -> bool:
        ...


class SupportsGe(Protocol):
    def __ge__(self: T, other: T, /) -> bool:
        ...


class SupportsLt(Protocol):
    def __lt__(self: T, other: T, /) -> bool:
        ...


class SupportsLe(Protocol):
    def __le__(self: T, other: T, /) -> bool:
        ...


class SupportsMod(Protocol):
    def __mod__(self: T, other: T, /) -> T:
        ...


class SupportsDiv(Protocol):
    def __div__(self: T, other: T, /) -> T:
        ...
