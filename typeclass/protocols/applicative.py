from typing import TypeVar, Protocol, Generic, Callable, Self
from typeclass.protocols.functor import Functor

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Applicative(Functor[A], Protocol, Generic[A]):
    """
    Applicative is a typeclass that extends Functor by providing two essential operations:
    - `pure`: embeds a raw value into the applicative context.
    - `ap`: applies a function wrapped in a context to a value wrapped in the same context.

    All Applicative instances must satisfy the following laws:

        Identity:
            v.ap(cls.pure(lambda x: x)) == v

        Homomorphism:
            cls.pure(x).ap(cls.pure(f)) == cls.pure(f(x))

        Interchange:
            cls.pure(y).ap(u) == u.ap(cls.pure(lambda f: f(y)))

        Composition:
            u.ap(v.ap(w.ap(cls.pure(lambda f: lambda g: lambda x: f(g(x)))))) ==
            u.ap(v).ap(w)
    """

    def ap(self, ff: "Applicative[Callable[[A], B]]") -> "Applicative[B]":
        """
        Apply a function wrapped in the applicative context to this wrapped value.

        Example:
            Box(5).ap(Box(lambda x: x + 1)) -> Box(6)

        Note: This is the applicative analog of function application.
        """
        ...

    @classmethod
    def pure(cls, value: A) -> Self:
        """
        Embed a raw value into the applicative context.

        Example:
            Box.pure(5) -> Box(5)

        This should satisfy:
            cls.pure(f).ap(cls.pure(x)) == cls.pure(f(x))
        """
        ...

def ap(fa: Applicative[A], ff: Applicative[Callable[[A], B]]) -> Applicative[B]:
    """
    Apply a function wrapped in an applicative context to a value wrapped in the same context.

    This is the standalone version of `fa.ap(ff)`, matching Haskell's `<*>`.

    Args:
        ff: An Applicative containing a function from A to B.
        fa: An Applicative containing a value of type A.

    Returns:
        An Applicative containing the result of applying the function to the value.
    """
    return fa.ap(ff)

def pure(cls: type, value: A):
    return cls.pure(value)

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
    return fa.fmap(lambda a: lambda b: f(a, b)).ap(fb)

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
