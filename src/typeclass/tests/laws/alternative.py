from typing import TypeVar
from typeclass.protocols.applicative import Applicative
from typeclass.syntax.symbols import pure, fmap, bind, empty, otherwise, some, many

A = TypeVar("A")


def alternative_left_identity_expr(cls: type, value):
    """
    Left identity:
        empty <|> x == x
    """
    lhs = empty(cls) |otherwise| value
    rhs = value
    return lhs, rhs


def alternative_right_identity_expr(cls: type, value):
    """
    Right identity:
        x <|> empty == x
    """
    lhs = value |otherwise| empty(cls)
    rhs = value
    return lhs, rhs


def alternative_associativity_expr(x, y, z):
    """
    Associativity:
        (x <|> y) <|> z == x <|> (y <|> z)
    """
    lhs = (x |otherwise| y) |otherwise| z
    rhs = x |otherwise| (y |otherwise| z)
    return lhs, rhs


def alternative_some_expr(cls: type, value):
    """
    Derived Alternative operation:
        some(v) == v >>= \\x -> fmap (many v) (\\xs -> [x] + xs)
    """
    lhs = cls |some| value
    rhs = value |bind| (
        lambda x: (cls |many| value) |fmap| (lambda xs: [x] + xs)
    )
    return lhs, rhs


def alternative_many_expr(cls: type, value):
    """
    Derived Alternative operation:
        many(v) == some(v) <|> pure([])
    """
    lhs = cls |many| value
    rhs = (cls |some| value) |otherwise| (cls |pure| [])
    return lhs, rhs
