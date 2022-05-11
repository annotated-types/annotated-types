# annotated-types

[![CI](https://github.com/annotated-types/annotated-types/workflows/CI/badge.svg?event=push)](https://github.com/annotated-types/annotated-types/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![pypi](https://img.shields.io/pypi/v/annotated-types.svg)](https://pypi.python.org/pypi/annotated-types)
[![versions](https://img.shields.io/pypi/pyversions/annotated-types.svg)](https://github.com/annotated-types/annotated-types)
[![license](https://img.shields.io/github/license/annotated-types/annotated-types.svg)](https://github.com/annotated-types/annotated-types/blob/main/LICENSE)

[PEP-593](https://peps.python.org/pep-0593/) added `typing.Annotated` as a way of
adding context-specific metadata to existing types, and specifies that
`Annotated[T, x]` _should_ be treated as `T` by any tool or library without special
logic for `x`.

This package provides metadata objects which can be used to represent common
constraints such as upper and lower bounds on scalar values and collection sizes,
a `Predicate` marker for runtime checks, and [non-normative](https://developer.mozilla.org/en-US/docs/Glossary/non-normative)
descriptions of how we intend these metadata to be interpreted. In some cases,
we also note alternative representations which do not require this package.

## Install

```bash
pip install annotated-types
```

## Examples

```python
from typing import Annotated
from annotated_types import Gt, Len

class MyClass:
    age: Annotated[int, Gt(18)]
    factors: list[Annotated[int, Predicate(is_prime)]]

    my_list: Annotated[list[int], 0:10]
    your_set: Annotated[set[int], Len(0, 10)]
```

## Documentation

_While `annotated-types` avoids runtime validation for performance\, users should not
construct invalid combinations such as `MultipleOf("non-numeric")` or `Annotated[int, Len(3)]`.
Downstream implementors may choose to raise an error, emit a warning, silently ignore
a metadata item, etc., if the metadata objects described below are used with an
incompatible type - or for any other reason!_

### Gt, Ge, Lt, Le

Express inclusive and/or exclusive bounds on orderable values - which may be numbers,
dates, times, strings, sets, etc. Note that the boundary value need not be of the
same type that was annotated, so long as they can be compared: `Annotated[int, Gt(1.5)]`
is fine, for example, and implies that the value is an integer x such that `x > 1.5`.
No interpretation is specified for special values such as `nan`.

We suggest that implementors may also interpret `functools.partial(operator.le, 1.5)`
as being equivalent to `Gt(1.5)`, for users who wish to avoid a runtime dependency on
the `annotated-types` package.

### Interval

`Interval(gt, ge, lt, le)` allows you to specify an upper and lower bound with a single
metadata object. `None` attributes should be ignored, and non-`None` attributes
treated as per the single bounds above.

### MultipleOf

`MultipleOf(multiple_of=x)` might be interpreted in two ways:

1. Python semantics, implying `value % multiple_of == 0`, or
2. [JSONschema semantics](https://json-schema.org/draft/2020-12/json-schema-validation.html#rfc.section.6.2.1),
   where `int(value / multiple_of) == value / multiple_of`.

We encourage users to be aware of these two common interpretations and their
distinct behaviours, and libraries to carefully document which they implement.

### Len

Len() implies that `min_inclusive <= len(value) < max_exclusive`.
We recommend that libraries interpret `slice` objects identically
to Len(), making all the following cases equivalent:

- `Annotated[list, :10]`
- `Annotated[list, 0:10]`
- `Annotated[list, None:10]`
- `Annotated[list, slice(0, 10)]`
- `Annotated[list, Len(0, 10)]`
- `Annotated[list, Len(max_exclusive=10)]`

Implementors: note that Len() should always have an integer value for
`min_inclusive`, but `slice` objects can also have `start=None`.

### Regex

The interpretation of `Regex()` is not yet specified. (coming soon!)

### Timezone

`Timezone` can be used with a `datetime` or a `time` to express which timezones
are allowed. `Annotated[datetime, Timezone[None]]` must be a naive datetime.
`Timezone[...]` ([literal ellipsis](https://docs.python.org/3/library/constants.html#Ellipsis))
expresses that any timezone-aware datetime is allowed. You may also pass a specific
timezone string or `timezone` object such as `Timezone[timezone.utc]` or
`Timezone["Africa/Abidjan"]` to express that you only allow a specific timezone,
though we note that this is often a symptom of poor design.

### Predicate

`Predicate(func: Callable)` expresses that `func(value)` is truthy for valid values.
Users should prefer the statically inspectable metadata above, but if you need
the full power and flexibility of arbitrary runtime predicates... here it is.

We provide a few predefined predicates for common string constraints:
`IsLower = Predicate(str.islower)`, `IsUpper = Predicate(str.isupper)`, and
`IsDigit = Predicate(str.isdigit)`. Users are encouraged to use methods which
can be given special handling, and avoid indirection like `lambda s: s.lower()`.

## Design & History

This package was designed at the PyCon 2022 sprints by the maintainers of Pydantic
and Hypothesis, with the goal of making it as easy as possible for end-users to
provide more informative annotations for use by runtime libraries.

It is deliberately minimal, and following PEP-593 allows considerable downstream
discretion in what (if anything!) they choose to support. Nonetheless, we expect
that staying simple and covering _only_ the most common use-cases will give users
and maintainers the best experience we can. If you'd like more - follow our lead
and define it downstream!
