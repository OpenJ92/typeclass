from __future__ import annotations
from typing import Generic, TypeVar, Callable, Iterable, Iterator

from dataclasses import dataclass

from typeclass.data.thunk import Thunk
from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.alternative import Alternative
from typeclass.protocols.monad import Monad
from typeclass.protocols.show import Show
from typeclass.protocols.force import Force

A = TypeVar("A")
B = TypeVar("B")

@dataclass(frozen=True)
class Sequence(Monad[A], Alternative, Applicative[A], Functor[A], Show, Generic[A]):

    # ----- Functor ---------------------------------------------------------

    def fmap(self: Sequence[A], f: Force[Callable[[A], B]]) -> Sequence[B]:
        _f = f.force()
        match self:
            case Cons(head=h, tail=t):
                return Cons(_f(h), t.fmap(f))
            case Nil():
                return Nil()

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> Sequence[A]:
        return Cons(value, Nil())

    def ap(self: Sequence[Callable[[A], B]], fa: Force[Sequence[A]]) -> Sequence[B]:
        """
        Cartesian product applicative:
          [f1,f2] <*> [a,b] = [f1(a), f1(b), f2(a), f2(b)]
        """
        fs = self
        xs = fa.force()

        match fs:
            case Cons(head=f, tail=rest):
                return concat(xs.fmap(Thunk(lambda: f)), rest.ap(fa))
            case Nil():
                return Nil()

    # ----- Alternative -----------------------------------------------------

    @classmethod
    def empty(cls: type) -> Sequence[A]:
        return Nil()

    def otherwise(self: Sequence[A], other: Force[Sequence[A]]) -> Sequence[A]:
        return concat(self, other.force())

    # ----- Monad -----------------------------------------------------------

    def bind(self: Sequence[A], mf: Force[Callable[[A], Sequence[B]]]) -> Sequence[B]:
        mf_ = mf.force()

        match self:
            case Cons(head=h, tail=t):
                return concat(mf_(h), t.bind(mf))
            case Nil():
                return Nil()

    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Sequence({list(iter(self))!r})"

    # ----- Eq ------------------------------------------------------------

    def __eq__(self: Sequence[A], other: Sequence[A]) -> bool:
        match (self, other):
            case (Cons(x, xs), Cons(y, ys)):
                return True and xs == ys
            case _:
                return False
        return True

    # ----- Convenience -----------------------------------------------------

    def __iter__(self) -> Iterator[A]:
        cur: Sequence[A] = self
        while True:
            match cur:
                case Cons(head=h, tail=t):
                    yield h
                    cur = t
                case Nil():
                    return


@dataclass(frozen=True)
class Cons(Sequence[A]): 
    head: A
    tail: Sequence[A]


@dataclass(frozen=True)
class Nil(Sequence[A]):
    pass

def concat(xs: Sequence[A], ys: Sequence[A]) -> Sequence[A]:
    match xs:
        case Cons(head=head, tail=tail):
            return Cons(head, concat(tail,ys))
        case Nil():
            return ys
