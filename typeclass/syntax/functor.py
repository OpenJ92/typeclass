from dataclasses import dataclass
from typeclass.protocols.functor import Functor
from typeclass.data.thunk import Thunk
from typing import TypeVar, Protocol, Callable, Generic, Self

A = TypeVar("A")
B = TypeVar("B")

@dataclass
class Map:
    func: Callable[[A], B]
    value: Functor[A]

def fmap(functor: Functor[A], f: Callable[[A], B]) -> Functor[B]:
    """
    Map a function over a functor using external syntax.

    This is the standalone equivalent of `functor.fmap(f)` and matches Haskell's `fmap`.

    Args:
        f: A function to apply.
        functor: A Functor instance.

    Returns:
        A new functor with the function applied.
    """
    return Map(f, Thunk(lambda:functor))

def replace(value: A, functor: Functor[B]) -> Functor[A]:
    """
    Replace all values in the functor with the given value.

    Equivalent to Haskell's `<$`.

    Args:
        value: The replacement value.
        functor: A Functor whose structure will be preserved.

    Returns:
        A new functor where every element is replaced with `value`.
    """
    return fmap(functor, lambda _: value)

def void(functor: Functor[A]) -> Functor[None]:
    """
    Replace all values in the functor with `None`.

    This is equivalent to Haskell's `void`, useful when you're only interested in the
    effects or structure and not the result.

    Args:
        functor: A Functor instance.

    Returns:
        A functor of the same shape with all values replaced by None.
    """
    return replace(None, functor)
