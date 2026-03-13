from typing import TypeVar
from typeclass.protocols.monoid import Monoid
from typeclass.syntax.symbols import combine, mempty

A = TypeVar("A", bound=Monoid)


def monoid_left_identity_expr(cls: type, value: A):
    """
    Left identity:
        mempty <> x == x
    """
    lhs = mempty(cls) |combine| value
    rhs = value
    return lhs, rhs


def monoid_right_identity_expr(cls: type, value: A):
    """
    Right identity:
        x <> mempty == x
    """
    lhs = value |combine| mempty(cls)
    rhs = value
    return lhs, rhs
