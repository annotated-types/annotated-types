import sys
from abc import ABC
from dataclasses import dataclass
from datetime import timezone
from typing import Any, Callable, Iterator, Optional, TypeVar, Union

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


T = TypeVar('T')


class ConstraintType(ABC):
    pass


if sys.version_info >= (3, 8):
    from annotated_types._compat38 import SupportsDiv, SupportsGe, SupportsGt, SupportsLe, SupportsLt, SupportsMod
else:
    from annotated_types._compat37 import SupportsDiv, SupportsGe, SupportsGt, SupportsLe, SupportsLt, SupportsMod


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
class Interval(ConstraintType):
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


@dataclass
class MultipleOf(ConstraintType):
    multiple_of: Union[SupportsDiv, SupportsMod]


@dataclass
class Len(ConstraintType):
    min_inclusive: int = 0
    max_exclusive: Optional[int] = None


@dataclass
class Regex(ConstraintType):
    regex_pattern: str
    regex_flags: int = 0


@dataclass
class Timezone(ConstraintType):
    tz: Union[str, timezone, EllipsisType, None] = ...


@dataclass
class Predicate(ConstraintType):
    func: Callable[[Any], bool]


IsLower = Predicate(str.islower)
IsUpper = Predicate(str.isupper)
IsDigit = Predicate(str.isdigit)
IsAscii = Predicate(str.isascii)
