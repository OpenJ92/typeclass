from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.protocols.semigroupoid import Semigroupoid
from typeclass.protocols.category import Category
from typeclass.protocols.arrow import Arrow
from typeclass.protocols.arrowchoice import ArrowChoice
from typeclass.protocols.arrowapply import ArrowApply
from typeclass.protocols.arrowloop import ArrowLoop

from typeclass.data.either import Either, Left, Right

from typeclass.protocols.force import Force

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True)
class Morphism(ArrowApply, ArrowChoice, Arrow, Category, Semigroupoid, Generic[A, B]):
    """
    Base arrow A -> B.
    """

    _run: Callable[[A], B]

    def __call__(self, a: A) -> B:
        return self._run(a)
    
    # --- Semigroupoid / Category ---

    def compose(self: Morphism[B, C], other: Force[Morphism[A, B]]) -> Morphism[A, C]:
        def inner(a: A) -> C:
            function = other.force()
            return self(function(a))
        return Morphism(inner)

    @classmethod
    def id(cls) -> Morphism[A, A]:
        return Morphism(lambda x: x)

    # --- Arrow ---

    @classmethod
    def arrow(cls, f: Force[Callable[[A], B]]) -> Morphism[A, B]:
        return Morphism(f.force())

    @classmethod
    def first(cls, self: Force[Morphism[A, B]]) -> Morphism[tuple[A, C], tuple[B, C]]:
        def inner(pair: tuple[A, C]) -> tuple[B, C]:
            a, c = pair
            f = self.force()
            return (f(a), c)
        return Morphism(inner)

    # --- ArrowChoice ---

    @classmethod
    def left(cls, self: Force[Morphism[A, B]]) -> Morphism[Either[A, C], Either[B, C]]:
        def inner(e: Either[A, C]) -> Either[B, C]:
            match e:
                case Left(a):
                    return Left(self.force()(a))
                case Right(c):
                    return Right(c)

        return Morphism(inner)

    # --- ArrowApply ---

    @classmethod
    def app(cls) -> Morphism[tuple[Morphism[A, B], A], B]:
        def inner(pair: tuple[Morphism[A, B], A]) -> B:
            f, a = pair
            return f(a)

        return Morphism(inner)
