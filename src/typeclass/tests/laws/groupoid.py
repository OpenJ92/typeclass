from typing import TypeVar
from typeclass.typeclasses.groupoid import Groupoid
from typeclass.typeclasses.symbols import rcompose, identity, invert

A = TypeVar("A")
B = TypeVar("B")


def groupoid_left_invert_expr(cls: type, value: Groupoid[A, B]):
    """
    Left invert:
        inv(f) >>> f == id
    """
    lhs = invert(value) |rcompose| value
    rhs = identity(cls)
    return lhs, rhs


def groupoid_right_invert_expr(cls: type, value: Groupoid[A, B]):
    """
    Right invert:
        f >>> inv(f) == id
    """
    lhs = value |rcompose| invert(value)
    rhs = identity(cls)
    return lhs, rhs
