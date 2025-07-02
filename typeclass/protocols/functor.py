from typing import TypeVar, Protocol, Callable, Generic, Self
from dataclasses import dataclass

A = TypeVar("A")
B = TypeVar("B")

class Functor(Protocol, Generic[A]):
    """
    Functor is a typeclass representing a computational context that can be mapped over.

    A Functor must implement the `fmap` method, which applies a function to a wrapped value
    without altering the structure of the context.

    All Functor instances must satisfy the following laws:

        Identity:
            fmap id == id

        Composition:
            fmap (f . g) == fmap f . fmap g

    Examples:
        Box(3).fmap(lambda x: x + 1) -> Box(4)
    """

    def fmap(self, f: Callable[[A], B]) -> Self:
        """
        Apply a function to the value inside the context, preserving the structure.

        Args:
            f: A function from A to B.

        Returns:
            A new functor context with the function applied.

        Example:
            Box(2).fmap(lambda x: x * 3) -> Box(6)
        """
        ...
