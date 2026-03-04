from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.protocols.semigroupoid import Semigroupoid
from typeclass.protocols.category import Category
from typeclass.protocols.arrow import Arrow

from typeclass.data.thunk import Thunk

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True)
class Morphism(Arrow, Category, Semigroupoid, Generic[A, B]):
    """
    Base arrow A -> B.
    """

    _run: Callable[[A], B]

    def __call__(self, a: A) -> B:
        return self._run(a)

    def compose(self: Morphism[B, C], other: Thunk[Morphism[A, B]]) -> Morphism[A, C]:
        def inner(a: A) -> C:
            function = other.force()
            return self(function(a))
        return Morphism(inner)

    @classmethod
    def id(cls) -> Morphism[A, A]:
        return Morphism(lambda x: x)

    @classmethod
    def arrow(cls, f: Thunk[Callable[[A], B]]) -> Morphism[A, B]:
        return Morphism(f.force())

    def first(self: Morphism[A, B]) -> Morphism[tuple[A, C], tuple[B, C]]:
        def inner(pair: tuple[A, C]) -> tuple[B, C]:
            a, c = pair
            return (self(a), c)
        return Morphism(inner)
