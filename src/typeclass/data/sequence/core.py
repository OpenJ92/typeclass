from typing import Generic, TypeVar, Callable, Iterator
from dataclasses import dataclass

from typeclass.data.thunk import Thunk
from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.alternative import Alternative
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.semigroup import Semigroup
from typeclass.typeclasses.monoid import Monoid
from typeclass.typeclasses.force import Force

A = TypeVar("A")
B = TypeVar("B")


@dataclass(
    frozen=True,
    eq=False,
    repr=False,
    order=False,
    unsafe_hash=False,
)
class Sequence(
    Monoid,
    Semigroup,
    Monad[A],
    Alternative,
    Applicative[A],
    Functor[A],
    Show,
    Generic[A],
):
    _values: tuple[A, ...]

    # ----- Functor ---------------------------------------------------------

    def fmap(self: "Sequence[A]", f: Force[Callable[[A], B]]) -> "Sequence[B]":
        _f = f.force()
        return Sequence(tuple(_f(x) for x in self._values))

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> "Sequence[A]":
        return Sequence((value,))

    def ap(self: "Sequence[Callable[[A], B]]", fa: Force["Sequence[A]"]) -> "Sequence[B]":
        """
        Cartesian product applicative:
          [f1,f2] <*> [a,b] = [f1(a), f1(b), f2(a), f2(b)]
        """
        xs = fa.force()._values
        out: list[B] = []

        for f in self._values:
            for x in xs:
                out.append(f(x))

        return Sequence(tuple(out))

    # ----- Alternative -----------------------------------------------------

    @classmethod
    def empty(cls: type) -> "Sequence[A]":
        return Sequence(())

    def otherwise(self: "Sequence[A]", other: Force["Sequence[A]"]) -> "Sequence[A]":
        return Sequence(self._values + other.force()._values)

    # ----- Monad -----------------------------------------------------------

    def bind(self: "Sequence[A]", mf: Force[Callable[[A], "Sequence[B]"]]) -> "Sequence[B]":
        """
        Stack-safe flatMap, preserves order.
        """
        mf_ = mf.force()
        out: list[B] = []

        for x in self._values:
            out.extend(mf_(x)._values)

        return Sequence(tuple(out))

    # ----- Semigroup -------------------------------------------------------

    def combine(self: "Sequence[A]", other: Force["Sequence[A]"]) -> "Sequence[A]":
        return Sequence(self._values + other.force()._values)

    # ----- Monoid ----------------------------------------------------------

    @classmethod
    def mempty(cls):
        return Sequence(())

    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Sequence({list(self._values)!r})"

    # ----- Eq --------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Sequence) and self._values == other._values

    # ----- Convenience -----------------------------------------------------

    def __iter__(self) -> Iterator[A]:
        return iter(self._values)
