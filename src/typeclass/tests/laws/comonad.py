from typing import Callable, TypeVar
from typeclass.protocols.comonad import Comonad
from typeclass.syntax.symbols import fmap, extract, duplicate, extend

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def comonad_left_identity_expr(value: Comonad[A]):
    """
    Left identity:
        extend extract == id
    """
    lhs = value |extend| extract
    rhs = value
    return lhs, rhs


def comonad_right_identity_expr(value: Comonad[A], f: Callable[[Comonad[A]], B]):
    """
    Right identity:
        extract (extend f w) == f w
    """
    lhs = extract(value |extend| f)
    rhs = f(value)
    return lhs, rhs


def comonad_associativity_expr(
    value: Comonad[A],
    f: Callable[[Comonad[B]], C],
    g: Callable[[Comonad[A]], B],
):
    """
    Associativity:
        extend f (extend g w)
            ==
        extend (lambda x: f (extend g x)) w
    """
    lhs = (value |extend| g) |extend| f
    rhs = value |extend| (lambda x: f(x |extend| g))
    return lhs, rhs


def comonad_extend_expr(value: Comonad[A], f: Callable[[Comonad[A]], B]):
    """
    Derived Comonad operation:
        extend f == fmap f . duplicate
    """
    lhs = value |extend| f
    rhs = duplicate(value) |fmap| f
    return lhs, rhs


def comonad_duplicate_expr(value: Comonad[A]):
    """
    Derived Comonad operation:
        duplicate == extend id
    """
    lhs = duplicate(value)
    rhs = value |extend| (lambda x: x)
    return lhs, rhs


def comonad_extract_duplicate_expr(value: Comonad[A]):
    """
    Derived Comonad operation:
        extract . duplicate == id
    """
    lhs = extract(duplicate(value))
    rhs = value
    return lhs, rhs


def comonad_duplicate_associativity_expr(value: Comonad[A]):
    """
    Coassociativity:
        duplicate (duplicate w)
            ==
        fmap duplicate (duplicate w)
    """
    lhs = duplicate(duplicate(value))
    rhs = duplicate(value) |fmap| duplicate
    return lhs, rhs
