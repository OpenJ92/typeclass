from typing import TypeVar
from typeclass.protocols.group import Group
from typeclass.syntax.symbols import combine, mempty, inverse

A = TypeVar("A", bound=Group)


def group_left_inverse_expr(cls: type, value: A):
    """
    Left inverse:
        inverse(x) <> x == mempty
    """
    lhs = inverse(value) |combine| value
    rhs = mempty(cls)
    return lhs, rhs


def group_right_inverse_expr(cls: type, value: A):
    """
    Right inverse:
        x <> inverse(x) == mempty
    """
    lhs = value |combine| inverse(value)
    rhs = mempty(cls)
    return lhs, rhs
