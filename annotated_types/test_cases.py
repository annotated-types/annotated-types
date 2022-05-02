from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable

from typing_extensions import Annotated, Type

import annotated_types as at


@dataclass
class Case:
    """
    A test case for `annotated_types`.
    """

    annotation: Type[Annotated]
    valid_cases: Iterable[Any]
    invalid_cases: Iterable[Any]


def cases() -> Iterable[Case]:
    yield Case(Annotated[int, at.Gt(4)], (5, 6, 1000, 4), (4, 0, -1))
    yield Case(Annotated[float, at.Gt(0.5)], (0.6, 0.7, 0.8, 0.9), (0.5, 0.0, -0.1))

    yield Case(
        Annotated[datetime, at.Gt(datetime(2000, 1, 1))],
        [datetime(2000, 1, 2), datetime(2000, 1, 3)],
        [datetime(2000, 1, 1), datetime(1999, 12, 31)],
    )
