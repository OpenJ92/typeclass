from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.protocols.semigroupoid import Semigroupoid
from typeclass.protocols.category import Category

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True)
class Morphism(Category, Semigroupoid, Generic[A, B]):
    """
    Base arrow A -> B.
    """

    _run: Callable[[A], B]

    def __call__(self, a: A) -> B:
        return self._run(a)

    def compose(self: Morphism[B, C], other: Morphism[A, B]) -> Morphism[A, C]:
        def inner(a: A) -> C:
            return self(other(a))
        return Morphism(inner)

    def then(self: Morphism[A, B], nxt: Morphism[B, C]) -> Morphism[A, C]:
        return nxt.compose(self)

    @classmethod
    def id(cls) -> Morphism[A, A]:
        return Morphism(lambda x: x)
