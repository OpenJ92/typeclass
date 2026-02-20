from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, TypeVar, runtime_checkable, Self
from typeclass.protocols.alternative import Alternative
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

@dataclass
class Some:
    internal: type
    v: Thunk

@dataclass
class Many:
    internal: type
    v: Thunk


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


def some(internal: type, v: Thunk) -> Thunk:
    return Some(internal, Thunk(lambda: v))

def many(internal: type, v: Thunk) -> Thunk:
    return Many(internal, Thunk(lambda: v))


