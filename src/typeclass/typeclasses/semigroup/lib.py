from dataclasses import dataclass

from typeclass.typeclasses.semigroup import Semigroup
from typeclass.data.thunk import Thunk

@dataclass
class Combine:
    a: Thunk[Semigroup]
    b: Thunk[Semigroup]

def combine(a: Semigroup, b: Semigroup):
    """
    Combine two Semigroup values.

    Equivalent to `a.combine(b)` or `a <> b`.

    Represents associative binary combination.

    Combination must satisfy the associativity law:

        combine(a, combine(b, c))
        ==
        combine(combine(a, b), c)

    for all semigroup values `a`, `b`, and `c`.

    No identity element is required for a Semigroup.
    (See Monoid for the identity law.)

    Args:
        a (Semigroup): A semigroup value.
        b (Semigroup): A semigroup value.

    Returns:
        Semigroup: The combined semigroup value.
    """
    return Combine(Thunk(lambda: a), Thunk(lambda: b))
