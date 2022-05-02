from dataclasses import dataclass
from datetime import timezone
from typing import Any, Callable, Union

try:
    from types import EllipsisType
except ImportError:
    EllipsisType = type(Ellipsis)

try:
    from typing import Protocol
except ImportError:
    try:
        from typing_extensions import Protocol
    except ImportError:
        Protocol = object

__all__ = (
    'Gt',
    'Ge',
    'Lt',
    'Le',
    'Interval',
    'MultipleOf',
    'Len',
    'Timezone',
    'Predicate',
    'IsLower',
    'IsUpper',
    'IsDigit',
)


class SupportsGt(Protocol):
    def __gt__(self, other: Any) -> bool:
        ...


class SupportsLt(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...


class SupportsGe(Protocol):
    def __ge__(self, other: Any) -> bool:
        ...


class SupportsLe(Protocol):
    def __le__(self, other: Any) -> bool:
        ...


@dataclass
class Gt:
    bound: SupportsGt


@dataclass
class Ge:
    bound: SupportsGe


@dataclass
class Lt:
    bound: SupportsLt


@dataclass
class Le:
    bound: SupportsLe


@dataclass
class Interval:
    gt: Union[SupportsGt, None] = None
    ge: Union[SupportsGe, None] = None
    lt: Union[SupportsLt, None] = None
    le: Union[SupportsLe, None] = None

    def __iter__(self):
        if self.gt is not None:
            yield Gt(self.gt)
        if self.ge is not None:
            yield Ge(self.ge)
        if self.lt is not None:
            yield Lt(self.lt)
        if self.le is not None:
            yield Le(self.le)


class SupportsMod(Protocol):
    def __mod__(self, other: Any) -> bool:
        ...


class SupportsDiv(Protocol):
    def __div__(self, other: Any) -> bool:
        ...


@dataclass
class MultipleOf:
    multiple: Union[SupportsMod, SupportsDiv]


@dataclass
class Len:
    min_inclusive: int = 0
    max_exclusive: Union[int, None] = None


@dataclass
class Timezone:
    tz: Union[str, timezone, EllipsisType, None] = ...


@dataclass
class Predicate:
    func: Callable[[Any], bool]


IsLower = Predicate(str.islower)
IsUpper = Predicate(str.isupper)
IsDigit = Predicate(str.isdigit)
