from typing import Protocol, runtime_checkable, Self
from typeclass.protocols.monoid import Monoid


@runtime_checkable
class Group(Monoid, Protocol):
    """
    Group typeclass.

    A Group is a Monoid in which every element has an inverse.

    Core operations:
        combine : a -> a -> a      (often written <>)
        mempty  : a               (identity)
        invert  : a -> a          (inverse)

    Laws:
        Associativity:
            (x <> y) <> z == x <> (y <> z)

        Identity:
            mempty <> x == x
            x <> mempty == x

        Inverses:
            x <> invert(x) == mempty
            invert(x) <> x == mempty
    """

    def inverse(self) -> Self:
        """
        Return the inverse of this value.

        Must satisfy:
            self.combine(self.invert()) == type(self).mempty()
            self.invert().combine(self) == type(self).mempty()
        """
        ...
