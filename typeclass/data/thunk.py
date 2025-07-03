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
        value = self._thunk()
        while isinstance(value, Thunk):
            value = value.force()
        return value

    def __repr__(self):
        return f"Thunk({self._value!r})" if self._evaluated else "Thunk(<unevaluated>)"

