from dataclasses import dataclass
from typeclass.protocols.applicative import Applicative
from typeclass.data.thunk import Thunk
from typeclass.syntax.functor import fmap
from typing import TypeVar, Protocol, Generic, Callable, Self

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

@dataclass
class Ap:
    ff: Applicative[Callable[[A], B]]
    fa: Applicative[A]

@dataclass
class Pure:
    cls: type
    value: A

def ap(ff: Applicative[Callable[[A], B]], fa: Applicative[A]) -> Applicative[B]:
    """
    Apply a function wrapped in an applicative context to a value wrapped in the same context.

    This is the standalone version of `fa.ap(ff)`, matching Haskell's `<*>`.

    Args:
        ff: An Applicative containing a function from A to B.
        fa: An Applicative containing a value of type A.

    Returns:
        An Applicative containing the result of applying the function to the value.
    """
    return Ap(Thunk(lambda: ff), Thunk(lambda: fa))

def pure(cls: type, value: A):
    return Pure(cls, Thunk(lambda: value))

def liftA2(f: Callable[[A, B], C], fa: Applicative[A], fb: Applicative[B]) -> Applicative[C]:
    """
    Lift a binary function into the applicative context.

    Applies the function `f` to the results of `fa` and `fb` within the Applicative.

    Equivalent to:
        liftA2(f, fa, fb) == fa.fmap(lambda a: lambda b: f(a, b)).ap(fb)

    Example:
        liftA2(lambda x, y: x + y, Just(2), Just(3)) == Just(5)

    Args:
        f: A binary function to lift into the context.
        fa: An Applicative containing the first argument.
        fb: An Applicative containing the second argument.

    Returns:
        An Applicative containing the result of applying `f` to the values of `fa` and `fb`.
    """
    return ap(fmap(fa, lambda a: lambda b: f(a, b)), fb)

def then(fa: Applicative[A], fb: Applicative[B]) -> Applicative[B]:
    """
    Sequence two Applicative actions, discarding the result of the first.

    Equivalent to:
        then(fa, fb) == liftA2(lambda _, b: b, fa, fb)

    Example:
        then(Just(1), Just(2)) == Just(2)

    Args:
        fa: The first Applicative, whose value will be discarded.
        fb: The second Applicative, whose value will be preserved.

    Returns:
        An Applicative containing the result of `fb`.
    """
    return liftA2(lambda _, b: b, fa, fb)

def skip(fa: Applicative[A], fb: Applicative[B]) -> Applicative[A]:
    """
    Sequence two Applicative actions, discarding the result of the second.

    Equivalent to:
        skip(fa, fb) == liftA2(lambda a, _: a, fa, fb)

    Example:
        skip(Just(1), Just(2)) == Just(1)

    Args:
        fa: The first Applicative, whose value will be preserved.
        fb: The second Applicative, whose value will be discarded.

    Returns:
        An Applicative containing the result of `fa`.
    """
    return liftA2(lambda a, _: a, fa, fb)

## def optional(fa: Alternative[A]) -> Alternative[Optional[A]]
##     # Come back to this later.
