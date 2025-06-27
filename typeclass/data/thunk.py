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
        if not self._evaluated:
            self._value = self._thunk()
            self._evaluated = True

        # Now recursively force if it's still a thunk
        value = self._value
        while isinstance(value, Thunk):
            value = value.force()
        return value


    def fmap(self, f: Callable[[A], B]) -> Thunk:
        return Thunk(lambda: self.force().fmap(f))  # T must be a Functor


    def ap(self: Thunk[TF], ff: Thunk[TF]) -> Thunk[TF]:
        return Thunk(lambda: self.force().ap(ff.force()))  # TF must be an Applicative

    @classmethod
    def pure(cls: type, value: A):
        return Thunk(lambda: value)

    def otherwise(self: Thunk[TA], alt: Thunk[TA]) -> Thunk[TA]:
        return Thunk(lambda: self.force().otherwise(alt.force()))  # TA must be an Alternative

    @classmethod
    def empty(cls: type) -> Self:
        return Thunk(lambda:None)

    def __repr__(self):
        return f"Thunk({self._value!r})" if self._evaluated else "Thunk(<unevaluated>)"


from typeclass.syntax.symbols import pure, fmap, ap, otherwise

def some(v: Thunk, internal: type) -> Thunk:
    print("[some] Called")
    return Thunk(lambda: ((v |fmap| (lambda x: lambda xs: [x] + xs)) |ap| many(v, internal)) \
               |otherwise| Thunk(lambda: internal |pure| []))

def many(v: Thunk, internal: type) -> Thunk:
    print("[many] Called")
    return Thunk(lambda: some(v, internal) |otherwise| Thunk(lambda: internal |pure| []))

