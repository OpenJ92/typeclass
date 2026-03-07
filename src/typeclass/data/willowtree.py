from dataclasses import dataclass
from typing import Generic, TypeVar

from typeclass.data.thunk import Thunk
from typeclass.data.stream import Stream

A = TypeVar("A")


@dataclass(frozen=True)
class WillowTree(Generic[A]):
    node: Thunk[tuple[A, Stream[WillowTree[A]]]]
