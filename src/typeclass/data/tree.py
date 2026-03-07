from dataclasses import dataclass
from typing import Generic, TypeVar

from typeclass.data.seq import Seq

A = TypeVar("A")


@dataclass(frozen=True)
class Tree(Generic[A]):
    value: A
    children: Seq[Tree[A]]
