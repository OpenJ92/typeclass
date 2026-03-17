from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.eq import Eq
from typeclass.typeclasses.force import Force

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class Maybe(Monad[A], Applicative[A], Functor[A], Eq, Show, Generic[A]):
    """
    Optional container.

        Maybe[A] = Just[A] | Nothing

    The Functor / Applicative / Monad structure acts on the `Just`
    branch and propagates `Nothing`.
    """

    value: A | None

    # ----- Functor ---------------------------------------------------------

    def fmap(self, f: Force[Callable[[A], B]]) -> Maybe[B]:
        match self:
            case Just(value=value):
                return Just(f.force()(value))
            case Nothing():
                return Nothing()

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls, value: A) -> Maybe[A]:
        return Just(value)

    def ap(self: Maybe[Callable[[A], B]], fa: Force[Maybe[A]]) -> Maybe[B]:
        match self:
            case Just(value=f):
                x = fa.force()
                match x:
                    case Just(value=v):
                        return Just(f(v))
                    case Nothing():
                        return Nothing()
            case Nothing():
                return Nothing()

    # ----- Applicative -----------------------------------------------------

    def otherwise(self: Maybe[A], other: Maybe[A]) -> Maybe[A]:
        match self:
            case Just():
                return self
            case Nothing():
                return other.force()

    @classmethod
    def empty(cls: type) -> Self:
        return Nothing()

    # ----- Monad -----------------------------------------------------------

    def bind(self, mf: Force[Callable[[A], Maybe[B]]]) -> Maybe[B]:
        match self:
            case Just(value=v):
                return mf.force()(v)
            case Nothing():
                return Nothing()

    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        match self:
            case Just(value=v):
                return f"Just({v!r})"
            case Nothing():
                return "Nothing()"

    # ----- Eq --------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Maybe):
            return False
        return self.value == other.value


@dataclass(frozen=True)
class Just(Maybe[A]):
    value: A


@dataclass(frozen=True)
class Nothing(Maybe[None]):
    value: None = None
