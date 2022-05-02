from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Iterable

from typing_extensions import Annotated

import annotated_types as at


@dataclass
class Case:
    """
    A test case for `annotated_types`.
    """

    annotation: Any
    valid_cases: Iterable[Any]
    invalid_cases: Iterable[Any]


def cases() -> Iterable[Case]:
    yield Case(Annotated[int, at.Gt(4)], (5, 6, 1000), (4, 0, -1))
    yield Case(Annotated[float, at.Gt(0.5)], (0.6, 0.7, 0.8, 0.9), (0.5, 0.0, -0.1))
    yield Case(
        Annotated[datetime, at.Gt(datetime(2000, 1, 1))],
        [datetime(2000, 1, 2), datetime(2000, 1, 3)],
        [datetime(2000, 1, 1), datetime(1999, 12, 31)],
    )
    yield Case(
        Annotated[datetime, at.Gt(date(2000, 1, 1))],
        [date(2000, 1, 2), date(2000, 1, 3)],
        [date(2000, 1, 1), date(1999, 12, 31)],
    )
    yield Case(
        Annotated[datetime, at.Gt(Decimal('1.123'))],
        [Decimal('1.1231'), Decimal('123')],
        [Decimal('1.123'), Decimal('0')],
    )

    yield Case(Annotated[int, at.Ge(4)], (4, 5, 6, 1000, 4), (0, -1))
    yield Case(Annotated[float, at.Ge(0.5)], (0.5, 0.6, 0.7, 0.8, 0.9), (0.4, 0.0, -0.1))
    yield Case(
        Annotated[datetime, at.Ge(datetime(2000, 1, 1))],
        [datetime(2000, 1, 2), datetime(2000, 1, 3)],
        [datetime(2000, 1, 1), datetime(1999, 12, 31)],
    )

    yield Case(Annotated[int, at.Lt(4)], (0, -1), (4, 5, 6, 1000, 4))
    yield Case(Annotated[float, at.Lt(0.5)], (0.4, 0.0, -0.1), (0.5, 0.6, 0.7, 0.8, 0.9))
    yield Case(
        Annotated[datetime, at.Lt(datetime(2000, 1, 1))],
        [datetime(2000, 1, 1), datetime(1999, 12, 31)],
        [datetime(2000, 1, 2), datetime(2000, 1, 3)],
    )

    yield Case(Annotated[int, at.Le(4)], (4, 0, -1), (5, 6, 1000, 4))
    yield Case(Annotated[float, at.Le(0.5)], (0.5, 0.0, -0.1), (0.6, 0.7, 0.8, 0.9))
    yield Case(
        Annotated[datetime, at.Le(datetime(2000, 1, 1))],
        [datetime(2000, 1, 1), datetime(1999, 12, 31)],
        [datetime(2000, 1, 2), datetime(2000, 1, 3)],
    )

    yield Case(Annotated[int, at.Interval(gt=4)], (5, 6, 1000, 4), (4, 0, -1))
    yield Case(Annotated[int, at.Interval(gt=4, lt=10)], (5, 6), (4, 10, 1000, 0, -1))
    yield Case(Annotated[float, at.Interval(ge=0.5, le=1)], (0.5, 0.9, 1), (0.49, 1.1))
    yield Case(
        Annotated[datetime, at.Interval(gt=datetime(2000, 1, 1), le=datetime(2000, 1, 3))],
        [datetime(2000, 1, 2), datetime(2000, 1, 3)],
        [datetime(2000, 1, 1), datetime(2000, 1, 4)],
    )

    yield Case(Annotated[int, at.MultipleOf(multiple_of=3)], (0, 3, 9), (1, 2, 4))
    yield Case(Annotated[float, at.MultipleOf(multiple_of=0.5)], (0, 0.5, 1, 1.5), (0.4, 1.1))
