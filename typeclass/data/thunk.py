from __future__ import annotations
from typing import Callable, Generic, TypeVar

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.alternative import Alternative

A = TypeVar("A")
B = TypeVar("B")
T = TypeVar("T", bound=Functor)
TF = TypeVar("TF", bound=Applicative)
TA = TypeVar("TA", bound=Alternative)

class Thunk(Alternative, Applicative, Functor, Generic[T]):
    def __init__(self, thunk: Callable[[], T]):
        self._thunk = thunk
        self._evaluated = False
        self._value: T | None = None

    def force(self) -> T:
        # Now recursively force if it's still a thunk
        value = self._thunk()
        while isinstance(value, Thunk):
            value = value.force()
        return value

    ## def otherwise(self: Thunk[TA], other: Thunk[TA]) -> Thunk[TA]:
    ##     def defered():
    ##         a = self.force()
    ##         if a == type(a).empty():
    ##             return other.force()

    ##         b = other.force()
    ##         if b == type(b).empty():
    ##             return Thunk(lambda: type(b).empty())

    ##         return a.otherwise(b)
    ##     return Thunk(defered)

    ## @classmethod
    ## def empty(cls: type) -> Self:
    ##     return Thunk(lambda:None)

    def __repr__(self):
        return f"Thunk({self._value!r})" if self._evaluated else "Thunk(<unevaluated>)"


from typeclass.syntax.symbols import pure, fmap, ap, otherwise

def some(v: Thunk, internal: type) -> Thunk:
    return v |fmap| (lambda x: lambda xs: [x] + xs) |ap| Thunk(lambda: many(v, internal))

def many(v: Thunk, internal: type) -> Thunk:
    return Thunk(lambda: some(v, internal)) |otherwise| Thunk(lambda: internal |pure| [])

