import re
import sys
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Iterator, Type, Union

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_args, get_origin
else:
    from typing import Annotated, get_args, get_origin

import pytest

if TYPE_CHECKING:
    from _pytest.mark import ParameterSet

import annotated_types
from annotated_types.test_cases import Case, cases

Constraint = Union[annotated_types.ConstraintType, slice, "re.Pattern[bytes]", "re.Pattern[str]"]


def check_gt(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val > constraint.gt


def check_lt(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Lt)
    return val < constraint.lt


def check_ge(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Ge)
    return val >= constraint.ge


def check_le(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Le)
    return val <= constraint.le


def check_multiple_of(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.MultipleOf)
    return val % constraint.multiple_of == 0


def check_regex(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, (annotated_types.Regex, re.Pattern))
    if isinstance(constraint, annotated_types.Regex):
        return re.fullmatch(constraint.regex_pattern, val, flags=constraint.regex_flags) is not None
    return constraint.fullmatch(val) is not None


def check_len(constraint: Constraint, val: Any) -> bool:
    if isinstance(constraint, slice):
        constraint = annotated_types.Len(constraint.start or 0, constraint.stop)
    assert isinstance(constraint, annotated_types.Len)
    if constraint.min_inclusive is None:
        raise TypeError
    if len(val) < constraint.min_inclusive:
        return False
    if constraint.max_exclusive is not None and len(val) >= constraint.max_exclusive:
        return False
    return True


def check_predicate(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Predicate)
    return constraint.func(val)


def check_timezone(constraint: Constraint, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Timezone)
    assert isinstance(val, datetime)
    if isinstance(constraint.tz, str):
        return val.tzinfo is not None and constraint.tz == val.tzname()
    elif isinstance(constraint.tz, timezone):
        return val.tzinfo is not None and val.tzinfo == constraint.tz
    elif constraint.tz is None:
        return val.tzinfo is None
    # ellipsis
    return val.tzinfo is not None


Validator = Callable[[Constraint, Any], bool]


VALIDATORS: Dict[Type[Constraint], Validator] = {
    annotated_types.Gt: check_gt,
    annotated_types.Lt: check_lt,
    annotated_types.Ge: check_ge,
    annotated_types.Le: check_le,
    annotated_types.MultipleOf: check_multiple_of,
    annotated_types.Regex: check_regex,
    annotated_types.Predicate: check_predicate,
    annotated_types.Len: check_len,
    annotated_types.Timezone: check_timezone,
    re.Pattern: check_regex,
    slice: check_len,
}


def get_constraints(tp: type) -> Iterator[Constraint]:
    origin = get_origin(tp)
    assert origin is Annotated
    args = iter(get_args(tp))
    next(args)
    for arg in args:
        if isinstance(arg, (annotated_types.ConstraintType, re.Pattern, slice)):
            if isinstance(arg, annotated_types.Interval):
                for case in arg:
                    yield case
            else:
                yield arg


def is_valid(tp: type, value: Any) -> bool:
    for constraint in get_constraints(tp):
        if not VALIDATORS[type(constraint)](constraint, value):
            return False
    return True


def extract_valid_testcases(case: Case) -> "Iterable[ParameterSet]":
    for example in case.valid_cases:
        yield pytest.param(case.annotation, example, id=f"{case.annotation} is valid for {repr(example)}")


def extract_invalid_testcases(case: Case) -> "Iterable[ParameterSet]":
    for example in case.invalid_cases:
        yield pytest.param(case.annotation, example, id=f"{case.annotation} is invalid for {repr(example)}")


@pytest.mark.parametrize(
    "annotation, example", [testcase for case in cases() for testcase in extract_valid_testcases(case)]
)
def test_valid_cases(annotation: type, example: Any):
    assert is_valid(annotation, example) is True


@pytest.mark.parametrize(
    "annotation, example", [testcase for case in cases() for testcase in extract_invalid_testcases(case)]
)
def test_invalid_cases(annotation: type, example: Any):
    assert is_valid(annotation, example) is False
