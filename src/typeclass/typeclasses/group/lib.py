from dataclasses import dataclass

from typeclass.typeclasses.group import Group
from typeclass.data.thunk import Thunk

@dataclass
class Inverse:
    self: Thunk[Group]

def inverse(self: Group):
    """
    Invert a Group value.

    Equivalent to `a.inverse()`.

    Represents the unique inverse of `a` under the
    associative `combine` operation.

    The inverse must satisfy the group laws:

        combine(a, inverse(a)) == mempty()

        combine(inverse(a), a) == mempty()

    for any group value `a`.

    Inversion must also be involutive:

        inverse(inverse(a)) == a

    A Group extends a Monoid by requiring that every
    element has such an inverse.

    Args:
        a (Group): A group value.

    Returns:
        Group: The inverse of `a` under `combine`.
    """
    return Inverse(Thunk(lambda: self))
