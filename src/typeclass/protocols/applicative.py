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
            pure id <*> v == v

        Homomorphism:
            pure f <*> pure x == pure (f x)

        Interchange:
            u <*> pure y == pure ($ y) <*> u

        Composition:
            pure (.) <*> u <*> v <*> w == u <*> (v <*> w)
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
