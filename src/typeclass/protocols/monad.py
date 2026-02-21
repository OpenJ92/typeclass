from typing import TypeVar, Protocol, Generic, Callable, Self
from typeclass.protocols.applicative import Applicative

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Monad(Applicative[A], Protocol, Generic[A]):
    """
    Monad is a typeclass that extends Applicative by providing a mechanism
    for sequencing dependent computations.

    In addition to `pure` (from Applicative), Monad introduces:

    - `bind` (often written >>=): sequences a computation by
      feeding the unwrapped value of a monadic context into a function
      that returns a new monadic context.

    - `return`: an alias of `pure`. It embeds a raw value into the monadic context.
      It does not introduce new behavior beyond `pure`, but exists for
      semantic clarity in monadic sequencing.

    Intuitively:
        If Applicative models independent structure,
        Monad models dependent structure.

    All Monad instances must satisfy the following laws:

        Left Identity:
            return a >>= f == f a

        Right Identity:
            m >>= return == m

        Associativity:
            (m >>= f) >>= g == m >>= (lambda x: f x >>= g)

    Note:
        `return_` must behave identically to `pure`.
    """

    def bind(self, mab: Callable[[A], Monad[B]]) -> Monad[B]:
        """
        Sequence a computation by applying a function to the wrapped value,
        where the function itself returns a new monadic context.

        Example:
            Box(5).bind(lambda x: Box(x + 1)) -> Box(6)

        Note: This is the monadic analog of dependent function application.
        The result of the first computation determines the next computation.
        """
        ...

    @classmethod
    def return_(cls, value: A) -> "Monad[A]":
        """
        Embed a raw value into the monadic context.
    
        Example:
            Box.return_(5) -> Box(5)
    
        Note: `return_` must behave identically to `pure`.
        It does not introduce new behavior beyond Applicative.
        """
        ...
    
