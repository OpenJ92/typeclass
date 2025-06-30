from __future__ import annotations
from typing import Protocol, TypeVar, runtime_checkable, Self
from typeclass.protocols.applicative import Applicative

A = TypeVar("A")
A = TypeVar("B")

@runtime_checkable
class Alternative(Applicative, Protocol):
    """
    Alternative typeclass.

    Describes computations that support failure and choice.
    Extends Applicative with `empty` and `otherwise`.

    Laws:
        Left identity:      empty <|> x               == x
        Right identity:     x <|> empty               == x
        Associativity:      (x <|> y) <|> z           == x <|> (y <|> z)
        Distributivity:     f <*> (x <|> y)           == (f <*> x) <|> (f <*> y)
        Annihilation:       empty <*> x               == empty
    """

    @classmethod
    def empty(cls) -> Self:
        """
        Return the identity element for the alternative operation.

        Returns:
            Self: The neutral or failure value.
        """
        ...

    def otherwise(self, other: Self) -> Self:
        """
        Provide a fallback if the current value represents failure.

        Args:
            other (Self): Fallback value to use if `self` is empty.

        Returns:
            Self: Result of the alternative choice.
        """
        ...

def empty(cls: type[Alternative]) -> Alternative:
    """
    Return the identity element of the Alternative operation.

    Equivalent to `cls.empty()`. Represents failure or absence.

    Args:
        cls (type[Alternative]): The class implementing Alternative.

    Returns:
        Alt
    """
    return cls.empty()

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
    return fa.otherwise(fb)
