import sys
from dataclasses import dataclass
from datetime import timezone
from typing import Any, Callable, Iterator, Optional, TypeVar, Union

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

if sys.version_info < (3, 10):
    EllipsisType = type(Ellipsis)
    KW_ONLY = {}
    SLOTS = {}
else:
    from types import EllipsisType

    KW_ONLY = {"kw_only": True}
    SLOTS = {"slots": True}


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


T = TypeVar('T')


# arguments that start with __ are considered
# positional only
# see https://peps.python.org/pep-0484/#positional-only-arguments


class SupportsGt(Protocol):
    def __gt__(self: T, __other: T) -> bool:
        ...


class SupportsGe(Protocol):
    def __ge__(self: T, __other: T) -> bool:
        ...


class SupportsLt(Protocol):
    def __lt__(self: T, __other: T) -> bool:
        ...


class SupportsLe(Protocol):
    def __le__(self: T, __other: T) -> bool:
        ...


class SupportsMod(Protocol):
    def __mod__(self: T, __other: T) -> T:
        ...


class SupportsDiv(Protocol):
    def __div__(self: T, __other: T) -> T:
        ...


class BaseMetadata:
    pass


@dataclass(frozen=True, **SLOTS)
class Gt(BaseMetadata):
    gt: SupportsGt


@dataclass(frozen=True, **SLOTS)
class Ge(BaseMetadata):
    ge: SupportsGe


@dataclass(frozen=True, **SLOTS)
class Lt(BaseMetadata):
    lt: SupportsLt


@dataclass(frozen=True, **SLOTS)
class Le(BaseMetadata):
    le: SupportsLe


@dataclass(frozen=True, **KW_ONLY)
class Interval(BaseMetadata):
    gt: Union[SupportsGt, None] = None
    ge: Union[SupportsGe, None] = None
    lt: Union[SupportsLt, None] = None
    le: Union[SupportsLe, None] = None

    def __iter__(self) -> Iterator[BaseMetadata]:
        if self.gt is not None:
            yield Gt(self.gt)
        if self.ge is not None:
            yield Ge(self.ge)
        if self.lt is not None:
            yield Lt(self.lt)
        if self.le is not None:
            yield Le(self.le)


@dataclass(frozen=True, **SLOTS)
class MultipleOf(BaseMetadata):
    multiple_of: Union[SupportsDiv, SupportsMod]


@dataclass(frozen=True, **SLOTS)
class Len(BaseMetadata):
    min_inclusive: Annotated[int, Ge(0)] = 0
    max_exclusive: Optional[Annotated[int, Ge(0)]] = None


@dataclass(frozen=True, **SLOTS)
class Regex(BaseMetadata):
    regex_pattern: Union[str, bytes]
    regex_flags: int = 0


@dataclass(frozen=True, **SLOTS)
class Timezone(BaseMetadata):
    tz: Union[str, timezone, EllipsisType, None]


@dataclass(frozen=True, **SLOTS)
class Predicate(BaseMetadata):
    func: Callable[[Any], bool]


IsLower = Predicate(str.islower)
IsUpper = Predicate(str.isupper)
IsDigit = Predicate(str.isdigit)
IsAscii = Predicate(str.isascii)
