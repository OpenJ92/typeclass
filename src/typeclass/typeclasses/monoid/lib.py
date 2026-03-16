from dataclasses import dataclass

from typing import TypeVar

from typeclass.typeclasses.monoid import Monoid
from typeclass.data.thunk import Thunk

@dataclass
class MEmpty:
    cls: Thunk[Monoid]

def mempty(cls):
    """
    Identity element for a Monoid.

    Equivalent to `Monoid.mempty()` or the identity value
    for the `combine` operation.

    Represents the neutral element under associative
    combination.

    The identity element must satisfy the unit laws:

        combine(a, mempty()) == a

        combine(mempty(), a) == a

    for any monoid value `a`.

    A Monoid extends a Semigroup by adding this identity
    element in addition to associativity.

    Args:
        cls (Monoid): The monoid type for which to construct
            the identity element.

    Returns:
        Monoid: The identity value for `combine`.
    """
    return MEmpty(cls)
