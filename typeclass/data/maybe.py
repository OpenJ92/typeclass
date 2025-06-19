from typing import Generic, TypeVar, Callable, Iterable

from typeclass.protocols.functor import Functor

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Maybe(Functor[A], Generic[A]):
    def fmap(self, f: Callable[[A], B]) -> "Maybe[B]":
        match self:
            case Just(value):
                return Just(f(value))
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
