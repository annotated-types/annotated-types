from typing import Iterator

import pytest

from annotated_types import BaseMetadata, GroupedMetadata


def test_subclass_without_implementing_iter() -> None:
    with pytest.raises(TypeError):

        class Foo1(GroupedMetadata):
            pass

    class Foo2(GroupedMetadata):
        def __iter__(self) -> Iterator[BaseMetadata]:
            return super().__iter__()

    with pytest.raises(NotImplementedError):
        for _ in Foo2():
            pass
