from typing import Callable, TypeVar

from typeclass.typeclasses.arrow import Arrow
from typeclass.typeclasses.symbols import compose, rcompose, first, second, split, fanout, arrow, identity

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
X = TypeVar("X")


def arrow_identity_expr(witness: type[Arrow[A, B]]):
    """
    Arrow law:
        arr(id) == id
    """
    lhs = witness |arrow| (lambda x: x)
    rhs = identity(witness)
    return lhs, rhs


def arrow_composition_expr(
    witness: type[Arrow[A, C]],
    f: Callable[[A], B],
    g: Callable[[B], C],
):
    """
    Arrow law:
        arr(g . f) == arr(g) . arr(f)
    """
    lhs = witness |arrow| (lambda x: f(g(x)))
    rhs = (witness |arrow| f) |compose| (witness |arrow| g)
    return lhs, rhs


def arrow_first_identity_expr(witness: type[Arrow[A, B]]):
    """
    Arrow law:
        first(id) == id
    """
    lhs = witness |first| witness.id()
    rhs = identity(witness)
    return lhs, rhs


def arrow_first_composition_expr(
    witness: type[Arrow[A, C]],
    f: Arrow[A, B],
    g: Arrow[B, C],
):
    """
    Arrow law:
        first(g . f) == first(g) . first(f)
    """
    lhs = witness |first| (f |compose| g)
    rhs = (witness |first| f) |compose| (witness |first| g)
    return lhs, rhs


def arrow_second_expr(witness: type[Arrow[A, B]], value: Arrow[A, B]):
    """
    Derived Arrow operation:
        second(f) == swap >>> first(f) >>> swap
    """
    def swap(pair):
        x, y = pair
        return (y, x)

    swap = witness |arrow| (lambda pair: (pair[1], pair[0]))
    lhs = witness |second| value
    rhs =         (witness |arrow| swap)  \
        |rcompose| (witness |first| value) \
        |rcompose| (witness |arrow| swap)

    return lhs, rhs


def arrow_split_expr(
    witness: type[Arrow[A, B]],
    value1: Arrow[A, B],
    value2: Arrow[C, D],
):
    """
    Derived Arrow operation:
        f *** g == first(f) >>> second(g)
    """
    lhs = value1 |split| (witness, value2)
    rhs = (witness |first| value1) |rcompose| (witness |second| value2)
    return lhs, rhs


def arrow_fanout_expr(
    witness: type[Arrow[A, B]],
    value1: Arrow[A, B],
    value2: Arrow[A, C],
):
    """
    Derived Arrow operation:
        f &&& g == arr(dup) >>> (f *** g)
    """
    lhs = value1 |fanout| (witness, value2)
    rhs =         (witness |arrow| (lambda x: (x, x))) \
        |rcompose| (value1 |split| (witness, value2))
    return lhs, rhs
