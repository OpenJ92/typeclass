from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, TypeVar, runtime_checkable, Self
from typeclass.protocols.applicative import Applicative
from typeclass.syntax.functor import fmap
from typeclass.syntax.applicative import pure, ap
from typeclass.data.thunk import Thunk

A = TypeVar("A")
B = TypeVar("B")

@dataclass
class Empty:
    cls: type

@dataclass
class Otherwise:
    fa: Alternative
    fb: Alternative


def empty(cls: type[Alternative]) -> Alternative:
    """
    Return the identity element of the Alternative operation.

    Equivalent to `cls.empty()`. Represents failure or absence.

    Args:
        cls (type[Alternative]): The class implementing Alternative.

    Returns:
        Alt
    """
    return Empty(cls)
def otherwise(fa: Alternative, fb: Alternative) -> Alternative:
    """
    Provide a fallback between two Alternative values.

    Equivalent to `x.otherwise(y)`. Returns `x` if successful, otherwise `y`.

    Args:
        x (Alternative): First option.
        y (Alternative): Fallback option.

    Returns:
        Alternative: The first successful alternative.
    """
    return Otherwise(Thunk(lambda: fa), Thunk(lambda: fb))


def some(v: Thunk, internal: type) -> Thunk:
    return ap(fmap(v, (lambda x: lambda xs: [x] + xs)), Thunk(lambda: many(v, internal)))

def many(v: Thunk, internal: type) -> Thunk:
    return otherwise(Thunk(lambda: some(v, internal)), Thunk(lambda: pure(internal,[])))


