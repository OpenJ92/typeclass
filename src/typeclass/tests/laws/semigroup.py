from typing import TypeVar
from typeclass.protocols.semigroup import Semigroup
from typeclass.syntax.symbols import combine

A = TypeVar("A", bound=Semigroup)


def semigroup_associativity_expr(x: A, y: A, z: A):
    """
    Associativity law:
        (x <> y) <> z == x <> (y <> z)
    """
    lhs = (x |combine| y) |combine| z
    rhs = x |combine| (y |combine| z)
    return lhs, rhs
