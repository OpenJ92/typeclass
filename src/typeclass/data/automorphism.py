from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.data.endomorphism import Endomorphism
from typeclass.protocols.group import Group

T = TypeVar("T")


@dataclass(frozen=True)
class Automorphism(Group, Endomorphism[T], Generic[T]):
    """
    Invertible endomorphism T <-> T.
    Group + Groupoid collapse here.
    """

    _run: Callable[[T], T]
    _inv: Callable[[T], T]

    def compose(self, other):
        function = other.force()
        match function:
            case Automorphism(_run=frun, _inv=finv):
                def fwd(t: T) -> T:
                    return self(frun(t))

                def bwd(t: T) -> T:
                    return finv(self._inv(t))

                return Automorphism(fwd, bwd)
            case _:
                return super().compose(other)

    def combine(self, other: Automorphism[T]) -> Automorphism[T]:
        return self.compose(other)

    @classmethod
    def mempty(cls) -> Automorphism[T]:
        return Automorphism(lambda x: x, lambda x: x)

    def inverse(self) -> Automorphism[T]:
        return Automorphism(self._inv, self._run)
