from typing import TypeVar, Protocol, Callable, Generic
from typing_extensions import Self

A = TypeVar("A")
B = TypeVar("B")

class Functor(Protocol, Generic[A]):
    """
    A type constructor f[_] that supports mapping a function over its contents.

    This protocol assumes:
    - The implementing type is generic over a single parameter (A)
    - fmap preserves the container structure (returns the same type)
    - fmap satisfies identity and composition laws (see test suite)
    """

    def fmap(self, f: Callable[[A], B]) -> Self:
        """
        Applies a function to the contents of the Functor.
        Returns a new instance of the same Functor with the function applied.
        """
        raise NotImplementedError

def fmap(f: Callable[[A], B], functor: Functor[B]) -> Functor[A]:
    """
    Applies a function to the contents of the Functor.
    Returns a new instance of the same Functor with the function applied.
    """
    return functor.fmap(f)

def replace(value: A, functor: Functor[B]) -> Functor[A]:
    """
    Replaces all values inside the functor with a single value.
    Equivalent to Haskell's (<$).
    """
    return functor.fmap(lambda _: value)

def void(functor: Functor[A]) -> Functor[None]:
    """
    Replaces all contents of the functor with None.
    Equivalent to Haskell's `void`.
    """
    return replace(None, functor)
