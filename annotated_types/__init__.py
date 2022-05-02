import sys
from abc import ABC
from dataclasses import dataclass
from datetime import timezone
from typing import Any, Callable, Iterator, Optional, TypeVar, Union

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

if sys.version_info < (3, 10):
    EllipsisType = type(Ellipsis)  # type: ignore[misc]
else:
    from types import EllipsisType


__all__ = (
    'Gt',
    'Ge',
    'Lt',
    'Le',
    'Interval',
    'MultipleOf',
    'Len',
    'Regex',
    'Timezone',
    'Predicate',
    'IsLower',
    'IsUpper',
    'IsDigit',
    '__version__',
)

__version__ = '0.2.0'


class ConstraintType(ABC):
    pass


class SupportsGt(Protocol):
    def __gt__(self, other: Any) -> bool:
        ...


class SupportsGe(Protocol):
    def __ge__(self, other: Any) -> bool:
        ...


class SupportsLt(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...


class SupportsLe(Protocol):
    def __le__(self, other: Any) -> bool:
        ...


@dataclass
class Gt(ConstraintType):
    gt: SupportsGt


@dataclass
class Ge(ConstraintType):
    ge: SupportsGe


@dataclass
class Lt(ConstraintType):
    lt: SupportsLt


@dataclass
class Le(ConstraintType):
    le: SupportsLe


@dataclass
class Interval:
    gt: Union[SupportsGt, None] = None
    ge: Union[SupportsGe, None] = None
    lt: Union[SupportsLt, None] = None
    le: Union[SupportsLe, None] = None

    def __iter__(self) -> Iterator[ConstraintType]:
        if self.gt is not None:
            yield Gt(self.gt)
        if self.ge is not None:
            yield Ge(self.ge)
        if self.lt is not None:
            yield Lt(self.lt)
        if self.le is not None:
            yield Le(self.le)


T = TypeVar('T')


class SupportsMod(Protocol):
    def __mod__(self: T, other: Any) -> T:
        ...


class SupportsDiv(Protocol):
    def __div__(self: T, other: Any) -> T:
        ...


@dataclass
class MultipleOf:
    multiple_of: SupportsMod


@dataclass
class Len:
    min_inclusive: int = 0
    max_exclusive: Optional[int] = None


@dataclass
class Regex:
    regex_pattern: str
    regex_flags: int = 0


@dataclass
class Timezone:
    tz: Union[str, timezone, EllipsisType, None] = ...


@dataclass
class Predicate:
    func: Callable[[Any], bool]


IsLower = Predicate(str.islower)
IsUpper = Predicate(str.isupper)
IsDigit = Predicate(str.isdigit)
IsAscii = Predicate(str.isascii)
