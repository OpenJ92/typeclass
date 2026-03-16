from typing import Protocol, runtime_checkable, Self
from typeclass.typeclasses.semigroup import Semigroup


@runtime_checkable
class Monoid(Semigroup, Protocol):
    """
    Monoid typeclass.

    A Monoid is a Semigroup with an identity element.

    Core operations:
        combine : a -> a -> a      (often written <>)
        mempty   : a               (identity)

    Laws:
        Associativity:
            (x <> y) <> z == x <> (y <> z)

        Left identity:
            mempty <> x == x

        Right identity:
            x <> mempty == x
    """

    @classmethod
    def mempty(cls) -> Self:
        """
        Return the identity element for `combine`.

        Returns:
            Self: The identity element.

        Must satisfy:
            cls.mempty().combine(x) == x
            x.combine(cls.mempty()) == x
        """
        ...
