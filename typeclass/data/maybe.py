from typing import Generic, TypeVar, Callable, Iterable

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Maybe(Applicative[A], Functor[A], Show, Eq, Generic[A]):
    def fmap(self, f: Callable[[A], B]) -> "Maybe[B]":
        match self:
            case Just(value=value):
                return Just(f(value))
            case Nothing():
                return Nothing()

    def ap(self: "Maybe[Callable[[A], B]]", fa: "Maybe[A]") -> "Maybe[B]":
        """
        Applies a function wrapped in a Maybe to another Maybe-wrapped value.
        Behaves like Haskell's `<*>` for Maybe:
            - Just(f) <*> Just(x) == Just(f(x))
            - Nothing <*> _       == Nothing
            - _ <*> Nothing       == Nothing
        """
        match self, fa:
            case Just(value=f), Just(value=x):
                return Just(f(x))
            case _:
                return Nothing()

    @classmethod
    def pure(cls, value: A) -> "Maybe[A]":
        """
        Embeds a value into the Maybe context.
        Equivalent to Haskell's `pure`.
        """
        return Just(value)

class Just(Maybe[A]):
    def __init__(self, value: A):
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Just) and self.value == other.value

    def __repr__(self):
        return f"Just({self.value})"


class Nothing(Maybe[A]):
    def __repr__(self):
        return "Nothing()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Nothing)

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
