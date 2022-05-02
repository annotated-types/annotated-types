# annotated-types

[![CI](https://github.com/annotated-types/annotated-types/workflows/CI/badge.svg?event=push)](https://github.com/annotated-types/annotated-types/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![pypi](https://img.shields.io/pypi/v/annotated-types.svg)](https://pypi.python.org/pypi/annotated-types)
[![versions](https://img.shields.io/pypi/pyversions/annotated-types.svg)](https://github.com/annotated-types/annotated-types)
[![license](https://img.shields.io/github/license/annotated-types/annotated-types.svg)](https://github.com/annotated-types/annotated-types/blob/main/LICENSE)

Reusable constraint types to use with `typing.Annotated`.

## Install

```bash
pip install annotated-types
```


example:

```python
from typing import Annotated, List
from annotated_types import Gt, Len

class MyClass:
    foobar: Annotated[int, Gt(4)]
    my_list: Annotated[List[int], 0:10]
    my_list_also: Annotated[List[int], Len(0, 10)]
```
