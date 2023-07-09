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
a `Predicate` marker for runtime checks, and
descriptions of how we intend these metadata to be interpreted. In some cases,
we also note alternative representations which do not require this package.

## Install

```bash
pip install annotated-types
```

## Examples

```python
from typing import Annotated
from annotated_types import Gt, Len, Predicate

class MyClass:
    age: Annotated[int, Gt(18)]                         # Valid: 19, 20, ...
                                                        # Invalid: 17, 18, "19", 19.0, ...
    factors: list[Annotated[int, Predicate(is_prime)]]  # Valid: 2, 3, 5, 7, 11, ...
                                                        # Invalid: 4, 8, -2, 5.0, "prime", ...

    my_list: Annotated[list[int], Len(0, 10)]           # Valid: [], [10, 20, 30, 40, 50]
                                                        # Invalid: (1, 2), ["abc"], [0] * 20
```

## Documentation

_While `annotated-types` avoids runtime checks for performance, users should not
construct invalid combinations such as `MultipleOf("non-numeric")` or `Annotated[int, Len(3)]`.
Downstream implementors may choose to raise an error, emit a warning, silently ignore
a metadata item, etc., if the metadata objects described below are used with an
incompatible type - or for any other reason!_

### Gt, Ge, Lt, Le

Express inclusive and/or exclusive bounds on orderable values - which may be numbers,
dates, times, strings, sets, etc. Note that the boundary value need not be of the
same type that was annotated, so long as they can be compared: `Annotated[int, Gt(1.5)]`
is fine, for example, and implies that the value is an integer x such that `x > 1.5`.

We suggest that implementors may also interpret `functools.partial(operator.le, 1.5)`
as being equivalent to `Gt(1.5)`, for users who wish to avoid a runtime dependency on
the `annotated-types` package.

To be explicit, these types have the following meanings:

* `Gt(x)` - value must be "Greater Than" `x` - equivalent to exclusive minimum
* `Ge(x)` - value must be "Greater than or Equal" to `x` - equivalent to inclusive minimum
* `Lt(x)` - value must be "Less Than" `x` - equivalent to exclusive maximum
* `Le(x)` - value must be "Less than or Equal" to `x` - equivalent to inclusive maximum

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
distinct behaviours, especially since very large or non-integer numbers make
it easy to cause silent data corruption due to floating-point imprecision.

We encourage libraries to carefully document which interpretation they implement.

### MinLen, MaxLen, Len

`Len()` implies that `min_length <= len(value) <= max_length` - lower and upper bounds are inclusive.

As well as `Len()` which can optionally include upper and lower bounds, we also
provide `MinLen(x)` and `MaxLen(y)` which are equivalent to `Len(min_length=x)`
and `Len(max_length=y)` respectively.

`Len`, `MinLen`, and `MaxLen` may be used with any type which supports `len(value)`.

Examples of usage:

* `Annotated[list, MaxLen(10)]` (or `Annotated[list, Len(max_length=10))`) - list must have a length of 10 or less
* `Annotated[str, MaxLen(10)]` - string must have a length of 10 or less
* `Annotated[list, MinLen(3))` (or `Annotated[list, Len(min_length=3))`) - list must have a length of 3 or more
* `Annotated[list, Len(4, 6)]` - list must have a length of 4, 5, or 6
* `Annotated[list, Len(8, 8)]` - list must have a length of exactly 8

#### Changed in v0.4.0

* `min_inclusive` has been renamed to `min_length`, no change in meaning
* `max_exclusive` has been renamed to `max_length`, upper bound is now **inclusive** instead of **exclusive**
* The recommendation that slices are interpreted as `Len` has been removed due to ambiguity and different semantic
  meaning of the upper bound in slices vs. `Len`

See [issue #23](https://github.com/annotated-types/annotated-types/issues/23) for discussion.

### Timezone

`Timezone` can be used with a `datetime` or a `time` to express which timezones
are allowed. `Annotated[datetime, Timezone(None)]` must be a naive datetime.
`Timezone[...]` ([literal ellipsis](https://docs.python.org/3/library/constants.html#Ellipsis))
expresses that any timezone-aware datetime is allowed. You may also pass a specific
timezone string or `timezone` object such as `Timezone(timezone.utc)` or
`Timezone("Africa/Abidjan")` to express that you only allow a specific timezone,
though we note that this is often a symptom of fragile design.

### Predicate

`Predicate(func: Callable)` expresses that `func(value)` is truthy for valid values.
Users should prefer the statically inspectable metadata above, but if you need
the full power and flexibility of arbitrary runtime predicates... here it is.

We provide a few predefined predicates for common string constraints:

* `IsLower = Predicate(str.islower)`
* `IsUpper = Predicate(str.isupper)`
* `IsDigit = Predicate(str.isdigit)`
* `IsFinite = Predicate(math.isfinite)`
* `IsNotFinite = Predicate(Not(math.isfinite))`
* `IsNan = Predicate(math.isnan)`
* `IsNotNan = Predicate(Not(math.isnan))`
* `IsInfinite = Predicate(math.isinf)`
* `IsNotInfinite = Predicate(Not(math.isinf))`

Some libraries might have special logic to handle known or understandable predicates,
for example by checking for `str.isdigit` and using its presence to both call custom
logic to enforce digit-only strings, and customise some generated external schema.
Users are therefore encouraged to avoid indirection like `lambda s: s.lower()`, in
favor of introspectable methods such as `str.lower` or `re.compile("pattern").search`.
To enable basic negation of commonly used predicates like `math.isnan` without introducing introspection that makes it impossible for implementers to introspect the predicate we provide a `Not` wrapper that simply negates the predicate in an introspectable manner. Several of the predicates listed above are created in this manner.

We do not specify what behaviour should be expected for predicates that raise
an exception.  For example `Annotated[int, Predicate(str.isdigit)]` might silently
skip invalid constraints, or statically raise an error; or it might try calling it
and then propogate or discard the resulting
`TypeError: descriptor 'isdigit' for 'str' objects doesn't apply to a 'int' object`
exception.  We encourage libraries to document the behaviour they choose.

### Integrating downstream types with `GroupedMetadata`

Implementers may choose to provide a convenience wrapper that groups multiple pieces of metadata.
This can help reduce verbosity and cognitive overhead for users.
For example, an implementer like Pydantic might provide a `Field` or `Meta` type that accepts keyword arguments and transforms these into low-level metadata:

```python
from dataclasses import dataclass
from typing import Iterator
from annotated_types import GroupedMetadata, Ge

@dataclass
class Field(GroupedMetadata):
    ge: int | None = None
    description: str | None = None

    def __iter__(self) -> Iterator[object]:
        # Iterating over a GroupedMetadata object should yield annotated-types
        # constraint metadata objects which describe it as fully as possible,
        # and may include other unknown objects too.
        if self.ge is not None:
            yield Ge(self.ge)
        if self.description is not None:
            yield Description(self.description)
```

Libraries consuming annotated-types constraints should check for `GroupedMetadata` and unpack it by iterating over the object and treating the results as if they had been "unpacked" in the `Annotated` type.  The same logic should be applied to the [PEP 646 `Unpack` type](https://peps.python.org/pep-0646/), so that `Annotated[T, Field(...)]`, `Annotated[T, Unpack[Field(...)]]` and `Annotated[T, *Field(...)]` are all treated consistently.

Libraries consuming annotated-types should also ignore any metadata they do not recongize that came from unpacking a `GroupedMetadata`, just like they ignore unrecognized metadata in `Annotated` itself.

Our own `annotated_types.Interval` class is a `GroupedMetadata` which unpacks itself into `Gt`, `Lt`, etc., so this is not an abstract concern.  Similarly, `annotated_types.Len` is a `GroupedMetadata` which unpacks itself into `MinLen` (optionally) and `MaxLen`.

### Consuming metadata

We intend to not be perspcriptive as to _how_ the metadata and constraints are used, but as an example of how one might parse constraints from types annotations see our [implementation in `test_main.py`](https://github.com/annotated-types/annotated-types/blob/f59cf6d1b5255a0fe359b93896759a180bec30ae/tests/test_main.py#L94-L103).

It is up to the implementer to determine how this metadata is used.
You could use the metadata for runtime type checking, for generating schemas or to generate example data, amongst other use cases.

## Design & History

This package was designed at the PyCon 2022 sprints by the maintainers of Pydantic
and Hypothesis, with the goal of making it as easy as possible for end-users to
provide more informative annotations for use by runtime libraries.

It is deliberately minimal, and following PEP-593 allows considerable downstream
discretion in what (if anything!) they choose to support. Nonetheless, we expect
that staying simple and covering _only_ the most common use-cases will give users
and maintainers the best experience we can. If you'd like more constraints for your
types - follow our lead, by defining them and documenting them downstream!
