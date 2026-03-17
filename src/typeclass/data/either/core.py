from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.eq import Eq
from typeclass.typeclasses.force import Force

L = TypeVar("L")
A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class Either(Monad[A], Applicative[A], Functor[A], Eq, Show, Generic[L, A]):
    """
    Sum type with two branches.

        Either[L, A] = Left[L] | Right[A]

    Functor / Applicative / Monad act on the `Right` branch and
    propagate `Left`.
    """

    value: object

    # ----- Functor ---------------------------------------------------------

    def fmap(self, f: Force[Callable[[A], B]]) -> Either[L, B]:
        match self:
            case Right(value=v):
                return Right(f.force()(v))
            case Left(value=v):
                return Left(v)

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls, value: A) -> Either[L, A]:
        return Right(value)

    def ap(self: Either[L, Callable[[A], B]], fa: Force[Either[L, A]]) -> Either[L, B]:
        match self:
            case Right(value=f):
                x = fa.force()
                match x:
                    case Right(value=v):
                        return Right(f(v))
                    case Left(value=e):
                        return Left(e)
            case Left(value=e):
                return Left(e)

    # ----- Monad -----------------------------------------------------------

    def bind(self, mf: Force[Callable[[A], Either[L, B]]]) -> Either[L, B]:
        match self:
            case Right(value=v):
                return mf.force()(v)
            case Left(value=e):
                return Left(e)

    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        match self:
            case Right(value=v):
                return f"Right({v!r})"
            case Left(value=v):
                return f"Left({v!r})"

    # ----- Eq --------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Either):
            return False
        return self.value == other.value


@dataclass(frozen=True)
class Left(Either[L, A]):
    value: L


@dataclass(frozen=True)
class Right(Either[L, A]):
    value: A
