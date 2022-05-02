import sys
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Iterator, Type

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_args, get_origin
else:
    from typing import Annotated, get_args, get_origin

import pytest

if TYPE_CHECKING:
    from _pytest.mark import ParameterSet

import annotated_types
from annotated_types.test_cases import Case, cases


def check_gt(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val > constraint.gt


def check_lt(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Lt)
    return val < constraint.lt


def check_ge(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Ge)
    return val >= constraint.ge


def check_le(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Le)
    return val <= constraint.le


def check_multiple_of(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.MultipleOf)
    return val % constraint.multiple_of == 0


Validator = Callable[[annotated_types.ConstraintType, Any], bool]


VALIDATORS: Dict[Type[annotated_types.ConstraintType], Validator] = {
    annotated_types.Gt: check_gt,
    annotated_types.Lt: check_lt,
    annotated_types.Ge: check_ge,
    annotated_types.Le: check_le,
    annotated_types.MultipleOf: check_multiple_of,
}


def get_constraints(tp: type) -> Iterator[annotated_types.ConstraintType]:
    origin = get_origin(tp)
    assert origin is Annotated
    args = iter(get_args(tp))
    next(args)
    for arg in args:
        if isinstance(arg, annotated_types.ConstraintType):
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
        yield pytest.param(case.annotation, example, id=f"{case.annotation} is valid for {example}")


def extract_invalid_testcases(case: Case) -> "Iterable[ParameterSet]":
    for example in case.invalid_cases:
        yield pytest.param(case.annotation, example, id=f"{case.annotation} is invalid for {example}")


@pytest.mark.parametrize(
    "annotation, example", [testcase for case in cases() for testcase in extract_valid_testcases(case)]
)
def test_valid_cases(annotation: type, example: Any):
    assert is_valid(annotation, example) is True
