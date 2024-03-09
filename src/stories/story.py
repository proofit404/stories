from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import TypeVar

T = TypeVar("T")


@contextmanager
def story(usecase: T) -> Iterator[T]:
    yield usecase
