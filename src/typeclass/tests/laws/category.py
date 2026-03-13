from typing import TypeVar
from typeclass.protocols.category import Category
from typeclass.syntax.symbols import compose, rcompose, identity

A = TypeVar("A")
B = TypeVar("B")


def category_left_identity_expr(cls: type, value: Category[A, B]):
    """
    Left identity:
        id >>> f == f
    """
    lhs = identity(cls) |compose| value
    rhs = value
    return lhs, rhs


def category_right_identity_expr(cls: type, value: Category[A, B]):
    """
    Right identity:
        f >>> id == f
    """
    lhs = value |compose| identity(cls)
    rhs = value
    return lhs, rhs


def category_left_ridentity_expr(cls: type, value: Category[A, B]):
    """
    Left reverse identity:
        id <<< f == f
    """
    lhs = identity(cls) |rcompose| value
    rhs = value
    return lhs, rhs


def category_right_ridentity_expr(cls: type, value: Category[A, B]):
    """
    Right reverse identity:
        f <<< id == f
    """
    lhs = value |rcompose| identity(cls)
    rhs = value
    return lhs, rhs
