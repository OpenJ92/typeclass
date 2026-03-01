from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.data.morphism import Morphism
from typeclass.protocols.semigroup import Semigroup
from typeclass.protocols.monoid import Monoid

T = TypeVar("T")


@dataclass(frozen=True)
class Endomorphism(Monoid, Semigroup, Morphism[T, T], Generic[T]):
    """
    Endomorphism T -> T.
    Monoid lives here.
    """

    _run: Callable[[T], T]

    def compose(self, other: Morphism[T, T]) -> Morphism[T, T]:
        function = other.force()
        match function:
            case Endomorphism():
                def inner(t: T) -> T:
                    return self(function(t))
                return Endomorphism(inner)
            case _:
                return super().compose(other)

    def combine(self, other: Endomorphism[T]) -> Endomorphism[T]:
        function = other.force()
        match function:
            case Endomorphism():
                def inner(t: T) -> T:
                    return self(function(t))
                return Endomorphism(inner)

    @classmethod
    def mempty(cls) -> Endomorphism[T]:
        return Endomorphism(lambda x: x)
