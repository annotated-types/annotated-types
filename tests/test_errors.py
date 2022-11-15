import pytest

from annotated_types import Len, X, len_X


@pytest.mark.parametrize(
    "source",
    """
(X > 1) > 1
(X > 1) >= 1
(X >= 1) > 1
(X >= 1) >= 1
(X == 1) > 1
(X == 1) >= 1
(X == 1) <= 1
(X == 1) < 1
(X <= 1) <= 1
(X <= 1) < 1
(X < 1) <= 1
(X < 1) < 1

(len_X > 1) > 1
(len_X > 1) >= 1
(len_X > 1) == 1
(len_X >= 1) > 1
(len_X >= 1) >= 1
(len_X >= 1) == 1
(len_X == 1) > 1
(len_X == 1) >= 1
(len_X == 1) == 1
(len_X == 1) <= 1
(len_X == 1) < 1
(len_X <= 1) == 1
(len_X <= 1) <= 1
(len_X <= 1) < 1
(len_X < 1) == 1
(len_X < 1) <= 1
(len_X < 1) < 1
""".splitlines(),
    ids=repr,
)
def test_valueerror_cases(source):
    if source.strip():
        with pytest.raises(ValueError):
            eval(source)


@pytest.mark.parametrize(
    "source",
    """
Len() > 1.0
Len() >= 1.0
Len() == 1.0
Len() <= 1.0
Len() < 1.0
len_X > 1.0
len_X >= 1.0
len_X == 1.0
len_X <= 1.0
len_X < 1.0
""".splitlines(),
    ids=repr,
)
def test_typeerror_cases(source):
    if source.strip():
        with pytest.raises(TypeError):
            eval(source)
