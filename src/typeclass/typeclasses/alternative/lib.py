from dataclasses import dataclass
from typing import Protocol, TypeVar, runtime_checkable, Self
from typeclass.typeclasses.alternative import Alternative
from typeclass.typeclasses.functor import fmap
from typeclass.typeclasses.applicative import pure, ap
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
    """
    Match one or more occurrences of an Alternative value.

    Equivalent to the recursive definition:

        some(v) = pure(cons) <*> v <*> many(v)

    Requires at least one successful match of `v`.

    If `v` fails, the entire computation fails.

    Args:
        internal (type): The Alternative implementation.
        v (Thunk): The Alternative computation to repeat.

    Returns:
        Alternative: One or more occurrences of `v`.
    """
    return Some(internal, Thunk(lambda: v))

def many(internal: type, v: Thunk) -> Thunk:
    """
    Match zero or more occurrences of an Alternative value.

    Equivalent to the recursive definition:

        many(v) = some(v) <|> pure(empty)

    Always succeeds, even if `v` fails.

    Represents repetition under the Alternative structure.

    Args:
        internal (type): The Alternative implementation.
        v (Thunk): The Alternative computation to repeat.

    Returns:
        Alternative: Zero or more occurrences of `v`.
    """
    return Many(internal, Thunk(lambda: v))


