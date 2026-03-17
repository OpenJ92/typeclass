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


def reverse(xs: Sequence[A]) -> Sequence[A]:
    out: Sequence[A] = Nil()
    cur = xs
    while isinstance(cur, Cons):
        out = Cons(cur.head, out)
        cur = cur.tail
    return out


def concat(xs: Sequence[A], ys: Sequence[A]) -> Sequence[A]:
    """
    Stack-safe append.
    """
    rev = reverse(xs)
    out: Sequence[A] = ys
    cur = rev
    while isinstance(cur, Cons):
        out = Cons(cur.head, out)
        cur = cur.tail
    return out


@dataclass(
    frozen=True,
    eq=False,
    repr=False,
    order=False,
    unsafe_hash=False
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
    # ----- Functor ---------------------------------------------------------

    def fmap(self: Sequence[A], f: Force[Callable[[A], B]]) -> Sequence[B]:
        _f = f.force()

        rev: Sequence[B] = Nil()
        cur = self
        while isinstance(cur, Cons):
            rev = Cons(_f(cur.head), rev)
            cur = cur.tail

        return reverse(rev)

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> Sequence[A]:
        return Cons(value, Nil())

    def ap(self: Sequence[Callable[[A], B]], fa: Force[Sequence[A]]) -> Sequence[B]:
        """
        Cartesian product applicative:
          [f1,f2] <*> [a,b] = [f1(a), f1(b), f2(a), f2(b)]
        Stack-safe, preserves order.
        """
        xs = fa.force()
        out: Sequence[B] = Nil()

        # Build in reverse function order so final reverse gives original order.
        fs_rev = reverse(self)
        cur_f = fs_rev
        while isinstance(cur_f, Cons):
            mapped = xs.fmap(Thunk(lambda f=cur_f.head: f))
            out = concat(reverse(mapped), out)
            cur_f = cur_f.tail

        return reverse(out)

    # ----- Alternative -----------------------------------------------------

    @classmethod
    def empty(cls: type) -> Sequence[A]:
        return Nil()

    def otherwise(self: Sequence[A], other: Force[Sequence[A]]) -> Sequence[A]:
        return concat(self, other.force())

    # ----- Monad -----------------------------------------------------------

    def bind(self: Sequence[A], mf: Force[Callable[[A], Sequence[B]]]) -> Sequence[B]:
        """
        Stack-safe flatMap, preserves order.
        """
        mf_ = mf.force()
        out: Sequence[B] = Nil()

        cur = reverse(self)
        while isinstance(cur, Cons):
            chunk = mf_(cur.head)
            out = concat(chunk, out)
            cur = cur.tail

        return out

    # ----- Semigroup -------------------------------------------------------

    def combine(self: Sequence[A], other: Force[Sequence[B]]):
        return concat(self, other.force())

    # ----- Monoid ----------------------------------------------------------

    @classmethod
    def mempty(cls):
        return Nil()

    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Sequence({list(iter(self))!r})"

    # ----- Eq --------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sequence):
            return False

        cur1 = self
        cur2 = other

        while isinstance(cur1, Cons) and isinstance(cur2, Cons):
            if cur1.head != cur2.head:
                return False
            cur1 = cur1.tail
            cur2 = cur2.tail

        return isinstance(cur1, Nil) and isinstance(cur2, Nil)

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


@dataclass(frozen=True, eq=False, repr=False, order=False, unsafe_hash=False)
class Cons(Sequence[A]):
    head: A
    tail: Sequence[A]

    def __repr__(self) -> str:
        return Sequence.__repr__(self)


@dataclass(frozen=True, eq=False, repr=False, order=False, unsafe_hash=False)
class Nil(Sequence[A]):
    def __repr__(self) -> str:
        return Sequence.__repr__(self)
    
