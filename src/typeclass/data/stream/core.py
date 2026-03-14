from dataclasses import dataclass
from typing import Generic, TypeVar

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.comonad import Comonad
from typeclass.protocols.show import Show
from typeclass.data.thunk import Thunk

A = TypeVar("A")

@dataclass(frozen=True)
class Stream(Applicative[A], Comonad[A], Functor[A], Show, Generic[A]):
    head: A
    tail: Thunk["Stream[A]"]

    # ----- Functor ---------------------------------------------------------

    def fmap(self, f: Force[Callable[[A], B]]) -> "Stream[B]":
        nf = f.force()
        return Stream(
            nf(self.head),
            Thunk(lambda: self.tail.force().fmap(Thunk(lambda: nf))),
        )

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls, value: A) -> "Stream[A]":
        return Stream(value, Thunk(lambda: cls.pure(value)))

    def ap(self: "Stream[Callable[[A], B]]", fa: Force["Stream[A]"]) -> "Stream[B]":
        xs = fa.force()
        return Stream(
            self.head(xs.head),
            Thunk(lambda: self.tail.force().ap(Thunk(lambda: xs.tail.force()))),
        )

    # ----- Comonad -----------------------------------------------------------

    def extract(self) -> A:
        return self.head

    def duplicate(self) -> "Stream[Stream[A]]":
        return Stream(
            self,
            Thunk(lambda: self.tail.force().duplicate()),
        )

    # ----- Show --------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Stream({self.head!r}, Thunk(<tail>))"

    def __iter__(self) -> Iterator[A]:
        cur: Stream[A] = self
        while True:
            yield cur.head
            cur = cur.tail.force()
