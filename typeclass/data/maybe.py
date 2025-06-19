from typing import Generic, TypeVar, Callable

from typeclass.protocols.functor import Functor

A = TypeVar("A")
B = TypeVar("B")

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

