from __future__ import annotations
from typing import Callable, Generic, TypeVar

from typeclass.protocol.force import Force

T = TypeVar("T", bound=Functor)

class Thunk(Force[T], Generic[T]):
    def __init__(self, thunk: Callable[[], T]):
        self._thunk = thunk
        self._evaluated = False
        self._value: T | None = None

    def force(self) -> T:
        if not self._evaluated:
            value = self._thunk()
            while isinstance(value, Thunk):
                value = value.force()
            self._value = value
            self._evaluated = True
        return self._value

    def __repr__(self):
        return f"Thunk({self._value!r})" if self._evaluated else "Thunk(<unevaluated>)"

