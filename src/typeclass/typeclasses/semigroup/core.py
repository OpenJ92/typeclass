from typing import Protocol, TypeVar, runtime_checkable, Self

A = TypeVar("A")


@runtime_checkable
class Semigroup(Protocol):
    """
    Semigroup typeclass.

    A Semigroup is a type that supports an associative binary operation.

    Core operation:
        combine : a -> a -> a      (often written <>)

    Laws:
        Associativity:
            (x <> y) <> z == x <> (y <> z)

    Notes:
        - Semigroup does NOT require an identity element. (That’s Monoid.)
        - This is purely about *combining values* of the same type.
    """

    def combine(self, other: Self) -> Self:
        """
        Combine two values of the same type.

        Args:
            other (Self): The value to combine with this one.

        Returns:
            Self: The combined value.

        Must satisfy associativity.
        """
        ...
