from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.data.morphism import Morphism
from typeclass.typeclasses.groupoid import Groupoid

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True)
class Isomorphism(Groupoid, Morphism[A, B], Generic[A, B]):
    """
    Invertible arrow A <-> B.
    """

    _run: Callable[[A], B]
    _inv: Callable[[B], A]

    def invert(self) -> Isomorphism[B, A]:
        return Isomorphism(self._inv, self._run)

    def compose(self: Isomorphism[B, C], other: Morphism[A, B]) -> Morphism[A, C]:
        function = other.force()
        match function:
            case Isomorphism(_run=frun, _inv=finv):
                def fwd(a: A) -> C:
                    return self(frun(a))

                def bwd(c: C) -> A:
                    return finv(self._inv(c))

                return Isomorphism(fwd, bwd)
            case _:
                return super().compose(other)
