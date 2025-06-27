from typing import TypeVar, Protocol, Callable, Generic, Self

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
    return functor.fmap(f)

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
    return functor.fmap(lambda _: value)

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
