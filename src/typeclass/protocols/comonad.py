from typing import TypeVar, Protocol, Generic, Callable
from typeclass.protocols.functor import Functor

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Comonad(Functor[A], Protocol, Generic[A]):
    """
    Comonad is the categorical dual of Monad. While Monad models
    dependent sequencing of computations that produce new contexts,
    Comonad models computations that *consume* context.

    In addition to `fmap` (from Functor), Comonad introduces:

    - `extract`: retrieves the focused value from a contextual structure.

    - `duplicate`: produces a new comonadic structure where each position
      contains the sub-context starting at that position.

    - `extend`: transforms the values of a comonadic structure by applying
      a function to each local context.

    Intuitively:
        If Monad models *building context through computation*,
        Comonad models *observing context through computation*.

    All Comonad instances must satisfy the following laws:

        Left Identity:
            extend extract == id

        Right Identity:
            extract (extend f w) == f w

        Associativity:
            extend f (extend g w)
                ==
            extend (lambda x: f (extend g x)) w

    Note:
        `extend` is typically definable from `duplicate` and `fmap`:

            extend f == fmap f . duplicate

        Implementations may choose to define `extend` directly for
        efficiency, but it must behave equivalently to the definition above.
    """

    def extract(self) -> A:
        """
        Retrieve the focused value from the comonadic context.

        Example:
            Stream(1, ...) .extract() -> 1

        Note: `extract` is the dual of Monad's `return`/`pure`.
        Instead of embedding a value into a context, it retrieves
        the value from an existing context.
        """
        ...

    def duplicate(self) -> Comonad[Comonad[A]]:
        """
        Duplicate the context so that each position contains
        its own local sub-context.

        Example (Stream intuition):

            [1,2,3,4,...].duplicate() ->
                [
                    [1,2,3,4,...],
                    [2,3,4,...],
                    [3,4,...],
                    ...
                ]

        Note:
            `duplicate` is the dual of Monad's `join`.
            Instead of flattening nested contexts, it expands
            a context into a structure of contexts.
        """
        ...
