from __future__ import annotations
from typing import Callable, Generic, TypeVar

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.alternative import Alternative

T = TypeVar("T")
U = TypeVar("U")

class Thunk(Functor, Generic[T]):
    def __init__(self, thunk: Callable[[], T]):
        self._thunk = thunk
        self._evaluated = False
        self._value: T | None = None

    def force(self) -> T:
        if not self._evaluated:
            self._value = self._thunk()
            self._evaluated = True
        return self._value

    def fmap(self, f: Callable[[T], U]) -> Thunk[U]:
        return Thunk(lambda: f(self.force()))
