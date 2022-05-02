import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Annotated, Any, Callable, Pattern, Protocol


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
    gt: SupportsGt | None = None
    ge: SupportsGe | None = None
    lt: SupportsLt | None = None
    le: SupportsLe | None = None

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
    multiple: SupportsMod | SupportsDiv


@dataclass
class Len:
    min_inclusive: int = 0
    max_exclusive: int | None = None


@dataclass
class Timezone:
    timezone: str | timezone | Ellipsis | None = ...


@dataclass
class Predicate:
    func: Callable[[Any], bool]


IsLower = Predicate(str.islower)
IsUpper = Predicate(str.isupper)


class Foo:
    a_dict: Annotated[dict[str, str], 5:10]
    a_list: Annotated[list[str], Len(1, 3)]
    bound_int: Annotated[int, Gt(2), Lt(10)]
    # bound_int_again: Annotated[int, 2:10]
    bound_float: Annotated[float, Gt(2.5), Lt(5.5)]
    # bound_float_again: Annotated[float, 2.5:5.5]
    str_regex: Annotated[str, re.compile("...", flags=re.A)]
    a: Annotated[str, Pattern[str]]
    date_range: Annotated[datetime, date(2020, 1, 1) :]

    dt: Annotated[datetime, Timezone(...)]
    dt2: Annotated[datetime, Timezone(timezone.utc)]
    dt2: Annotated[datetime, Timezone('Europe/London')]
    dt3: Annotated[datetime, Timezone(None)]
