import pytest

import annotated_types
from annotated_types.test_cases import Case, cases


def test_gt():
    gt = annotated_types.Gt(4)
    assert gt.gt == 4


@pytest.mark.parametrize("case", [pytest.param(c, id=repr(c.annotation)) for c in cases()])
def test_cases(case: Case):
    assert case.annotation
    assert case.valid_cases
    assert case.invalid_cases
