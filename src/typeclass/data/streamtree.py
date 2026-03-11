from dataclasses import dataclass
from typing import Generic, TypeVar

from typeclass.data.stream import Stream

A = TypeVar("A")


@dataclass(frozen=True)
class StreamTree(Generic[A]):
    value: A
    children: Stream[StreamTree[A]]
