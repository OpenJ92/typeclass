from typing import TypeVar, Protocol, Generic, Callable, Self
from typeclass.protocols.functor import Functor

A = TypeVar("A")
B = TypeVar("B")

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

    def ap(self, ff: "Applicative[Callable[[A], B]]") -> "Applicative[B]":
        """
        Apply a function wrapped in the applicative context to this wrapped value.

        Example:
            Box(5).ap(Box(lambda x: x + 1)) -> Box(6)

        Note: This is the applicative analog of function application.
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
