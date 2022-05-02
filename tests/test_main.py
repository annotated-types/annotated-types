import sys
from typing import Any, Callable, Dict, Iterator, Type, get_args, get_origin

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

import pytest

import annotated_types
from annotated_types.test_cases import Case, cases


def check_gt(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val > constraint.gt


def check_lt(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val < constraint.gt


def check_ge(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val >= constraint.gt


def check_le(constraint: annotated_types.ConstraintType, val: Any) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val <= constraint.gt


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
            yield arg


def is_valid(tp: type, value: Any) -> bool:
    for constraint in get_constraints(tp):
        if not VALIDATORS[type(constraint)](constraint, value):
            return False
    return True


@pytest.mark.parametrize("case", [pytest.param(c, id=repr(c.annotation)) for c in cases()])
def test_cases(case: Case):
    for example in case.valid_cases:
        assert is_valid(case.annotation, example) is True
    for example in case.invalid_cases:
        assert is_valid(case.annotation, example) is False
