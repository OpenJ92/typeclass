from __future__ import annotations
from typing import Protocol, TypeVar, runtime_checkable, Self
from .applicative import Applicative

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

def thunk(f: Callable[[], Alternative[A]]) -> Alternative[A]:
    return f()  # allows compatibility with strict ap/fmap/etc

def some(v: Callable[[], Alternative[A]]) -> Alternative[List[A]]:
    # equivalent to: some x = (:) <$> x <*> many x
    head = v()
    tail = lambda: many(v)
    return head.fmap(lambda x: lambda xs: [x] + xs).ap(thunk(tail))

def many(v: Callable[[], Alternative[A]]) -> Alternative[List[A]]:
    return some(v).otherwise(thunk(lambda: v().pure([])))

## def some(v: Callable[[], Alternative]) -> Alternative:
##     """
##     One or more repetitions of an effectful action.
## 
##     Equivalent to: some fa = fa <*> many fa
## 
##     Args:
##         fa (Alternative[Self]): The action to repeat.
## 
##     Returns:
##         Alternative[Self]: The result of one or more repetitions of `fa`.
##     """
##     return v().ap(lambda: many(v))
## 
## def many(v: Callable[[], Alternative]) -> Alternative:
##     """
##     Zero or more repetitions of an effectful action.
## 
##     Equivalent to: many fa = some fa <|> pure []
## 
##     Args:
##         fa (Alternative[Self]): The action to repeat.
## 
##     Returns:
##         Alternative[Self]: The result of zero or more repetitions of `fa`.
##     """
##     return some(v).otherwise(lambda: v().pure([]))
