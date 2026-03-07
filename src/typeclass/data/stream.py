from dataclasses import dataclass
from typing import Generic, TypeVar

from typeclass.data.thunk import Thunk

A = TypeVar("A")


@dataclass(frozen=True)
class Stream(Generic[A]):
    head: A
    tail: Thunk[Stream[A]]
