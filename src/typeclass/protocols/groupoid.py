from typing import Protocol, runtime_checkable, Self
from typeclass.protocols.category import Category


@runtime_checkable
class Groupoid(Category, Protocol):
    """
    Groupoid typeclass.

    A Groupoid is a Category in which every morphism has an inverse
    with respect to `compose`.

    Core operations:
        compose : composition
        id      : identity
        invert  : arrow inverse
    """

    def invert(self) -> Self:
        """
        Return the inverse morphism under `compose`.

        Must satisfy:
            self.compose(self.invert()) == type(self).id()
            self.invert().compose(self) == type(self).id()
        """
        ...
