from dataclasses import dataclass

from typing import TypeVar

from typeclass.typeclasses.groupoid import Groupoid
from typeclass.data.thunk import Thunk

@dataclass
class Invert:
    self: Thunk[Groupid]

def invert(self: Groupid):
    """
    Invert a Groupoid morphism.

    Equivalent to `fab.invert()`.

    Represents categorical inversion: produce the unique
    morphism `fba` such that `fab` and `fba` are mutual inverses.

    Inversion must satisfy the inverse laws:

        compose(fab, invert(fab))
        ==
        identity(B)

        compose(invert(fab), fab)
        ==
        identity(A)

    for any morphism `fab: A -> B`.

    Inversion must also be involutive:

        invert(invert(fab))
        ==
        fab

    Args:
        fab (Groupoid): A morphism from A to B.

    Returns:
        Groupoid: The inverse morphism from B to A.
    """
    return Invert(Thunk(lambda: self))
