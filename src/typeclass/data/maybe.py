from __future__ import annotations
from typing import Generic, TypeVar, Callable, Iterable

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.alternative import Alternative
from typeclass.protocols.monad import Monad
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Maybe(Monad, Alternative, Applicative[A], Functor[A], Show, Eq, Generic[A]):
    def fmap(self: Maybe[A], f: Callable[[A], B]) -> Maybe[B]:
        match self:
            case Just(value=value):
                return Just(f(value))
            case Nothing():
                return Nothing()

    def ap(self: Maybe[Callable[[A], B]], fa: Maybe[A]) -> Maybe[B]:
        match self:
            case Just(value=f):
                x = fa.force()
                match x:
                    case Just(value=x):
                        return Just(f(x))
        return Nothing()

    @classmethod
    def pure(cls: type, value: A) -> Self:
        return Just(value)

    def otherwise(self: Maybe[A], other: Maybe[A]) -> Maybe[A]:
        match self:
            case Just():
                return self
            case Nothing():
                return other.force()

    @classmethod
    def empty(cls: type) -> Self:
        return Nothing()

    def __eq__(self: Maybe[A], other: Maybe[A]) -> bool:
        match self, other:
            case Just(value=x), Just(value=y):
                return x == y
            case Nothing(), Nothing():
                return True
        return False

    def bind(self: Maybe[A], mf: Callable[[A], Maybe[B]]) -> Maybe[B]:
        match self:
            case Just(value=a):
                mf = mf.force()
                return mf(a)
            case Nothing():
                return Nothing()
        

class Just(Maybe[A]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self):
        return f"Just({self.value})"

class Nothing(Maybe[A]):
    def __repr__(self):
        return "Nothing()"

# ----- Additional Functions -----

def is_just(m: Maybe[A]) -> bool:
    return isinstance(m, Just)

def is_nothing(m: Maybe[A]) -> bool:
    return isinstance(m, Nothing)

def from_maybe(default: A, m: Maybe[A]) -> A:
    match m:
        case Just(value=value): return value
        case Nothing(): return default

def maybe(default: C, f: Callable[[A], C], m: Maybe[A]) -> C:
    match m:
        case Just(value=value): return f(value)
        case Nothing(): return default

def cat_maybes(ms: Iterable[Maybe[A]]) -> list[A]:
    return [m.value for m in ms if isinstance(m, Just)]

def map_maybe(f: Callable[[A], Maybe[B]], xs: Iterable[A]) -> list[B]:
    return [y.value for x in xs if (y := f(x)) and isinstance(y, Just)]
