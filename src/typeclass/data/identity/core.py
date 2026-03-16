from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.data.thunk import Thunk
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.comonad import Comonad
from typeclass.typeclasses.eq import Eq
from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.force import Force

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class Identity(Comonad[A], Monad[A], Applicative[A], Functor[A], Show, Eq, Generic[A]):
    """
    The trivial effect.

        Identity[A] = A

    Identity is useful as the base monad for transformer-specialized
    "ordinary" datatypes, e.g.

        Writer[W, A] = WriterT[W, Identity, A]
        Either[E, A] = EitherT[E, Identity, A]
    """

    value: A

    def run(self) -> A:
        return self.value

    def fmap(self, f: Force[Callable[[A], B]]) -> Identity[B]:
        return Identity(f.force()(self.value))

    @classmethod
    def pure(cls, value: A) -> Identity[A]:
        return cls(value)

    def ap(self: Identity[Callable[[A], B]], fa: Force[Identity[A]]) -> Identity[B]:
        return Identity(self.value(fa.force().value))

    def bind(self, fm: Force[Callable[[A], Identity[B]]]) -> Identity[B]:
        return fm.force()(self.value)

    def extract(self) -> A:
        return self.value

    def duplicate(self) -> Identity[Identity[A]]:
        return Identity(self)

    def show(self) -> str:
        return f"Identity({self.value!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Identity) and self.value == other.value
