from __future__ import annotations
from typing import Generic, TypeVar, Callable, Iterable, Iterator

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.alternative import Alternative
from typeclass.protocols.monad import Monad
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq

A = TypeVar("A")
B = TypeVar("B")


class Seq(Monad, Alternative, Applicative[A], Functor[A], Show, Eq, Generic[A]):
    # ----- Functor ---------------------------------------------------------

    def fmap(self: Seq[A], f: Callable[[A], B]) -> Seq[B]:
        match self:
            case Cons(head=h, tail=t):
                return Cons(f.force()(h), t.fmap(f))
            case Nil():
                return Nil()

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> Seq[A]:
        return Cons(value, Nil())

    def ap(self: Seq[Callable[[A], B]], fa: Seq[A]) -> Seq[B]:
        """
        Cartesian product applicative:
          [f1,f2] <*> [a,b] = [f1(a), f1(b), f2(a), f2(b)]
        """
        fs = self
        xs = fa.force()

        def map_all(f: Callable[[A], B], xs_: Seq[A]) -> Seq[B]:
            match xs_:
                case Cons(head=h, tail=t):
                    return Cons(f(h), map_all(f, t))
                case Nil():
                    return Nil()

        def concat(a: Seq[B], b: Seq[B]) -> Seq[B]:
            match a:
                case Cons(head=h, tail=t):
                    return Cons(h, concat(t, b))
                case Nil():
                    return b

        match fs:
            case Cons(head=f, tail=rest):
                return concat(map_all(f, xs), rest.ap(xs))
            case Nil():
                return Nil()

    # ----- Alternative -----------------------------------------------------

    @classmethod
    def empty(cls: type) -> Seq[A]:
        return Nil()

    def otherwise(self: Seq[A], other: Seq[A]) -> Seq[A]:
        """
        Choice for Seq = concatenation.
        """
        other_ = other.force()
        match self:
            case Cons(head=h, tail=t):
                return Cons(h, t.otherwise(other_))
            case Nil():
                return other_

    # ----- Monad -----------------------------------------------------------

    def bind(self: Seq[A], mf: Callable[[A], Seq[B]]) -> Seq[B]:
        mf_ = mf.force()

        def concat(a: Seq[B], b: Seq[B]) -> Seq[B]:
            match a:
                case Cons(head=h, tail=t):
                    return Cons(h, concat(t, b))
                case Nil():
                    return b

        match self:
            case Cons(head=h, tail=t):
                return concat(mf_(h), t.bind(mf_))
            case Nil():
                return Nil()

    # ----- Convenience -----------------------------------------------------

    def __iter__(self) -> Iterator[A]:
        cur: Seq[A] = self
        while True:
            match cur:
                case Cons(head=h, tail=t):
                    yield h
                    cur = t
                case Nil():
                    return

    def to_list(self) -> list[A]:
        return list(iter(self))

    @staticmethod
    def from_iterable(xs: Iterable[A]) -> Seq[A]:
        out: Seq[A] = Nil()
        # build from right to left
        tmp = list(xs)
        for x in reversed(tmp):
            out = Cons(x, out)
        return out

    def __repr__(self) -> str:
        return f"Seq({self.to_list()!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Seq):
            return False
        return self.to_list() == other.to_list()


class Cons(Seq[A]):
    def __init__(self, head: A, tail: Seq[A]):
        self.head = head
        self.tail = tail


class Nil(Seq[A]):
    pass
