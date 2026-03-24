from typing import Callable, TypeVar

from typeclass.typeclasses.arrowchoice import ArrowChoice
from typeclass.typeclasses.symbols import (
    identity,
    arrow,
    compose,
    rcompose,
    left,
    right,
    plusplus,
    oror,
)
from typeclass.data.either import Left, Right

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
X = TypeVar("X")


def arrowchoice_left_naturality_expr(
    witness: type[ArrowChoice[A, B]],
    f: Callable[[A], B],
):
    """
    ArrowChoice law:
        left(arr(f)) == arr(map_left(f))

    where:
        map_left(f)(Left(x))  = Left(f(x))
        map_left(f)(Right(y)) = Right(y)
    """
    def mapleft(f):
        def inner(either):
            match either:
                case Left(value=value):
                    return Left(f(value))
                case Right(value=value):
                    return Right(value)
        return inner

    lhs = witness |left|  (witness |arrow| f)
    rhs = witness |arrow| mapleft(f)
    return lhs, rhs


def arrowchoice_right_naturality_expr(
    witness: type[ArrowChoice[A, B]],
    f: Callable[[A], B],
):
    """
    ArrowChoice law:
        right(arr(f)) == arr(map_right(f))

    where:
        map_right(f)(Left(x))  = Left(x)
        map_right(f)(Right(y)) = Right(f(y))
    """
    def mapright(f):
        def inner(either):
            match either:
                case Left(value=value):
                    return Left(value)
                case Right(value=value):
                    return Right(f(value))
        return inner

    lhs = witness |right| (witness |arrow| f)
    rhs = witness |arrow| mapright(f)
    return lhs, rhs


def arrowchoice_left_identity_expr(witness: type[ArrowChoice[A, B]]):
    """
    ArrowChoice law:
        left(id) == id
    """
    lhs = witness |left| identity(witness)
    rhs = identity(witness)
    return lhs, rhs


def arrowchoice_right_identity_expr(witness: type[ArrowChoice[A, B]]):
    """
    ArrowChoice law:
        right(id) == id
    """
    lhs = witness |right| identity(witness)
    rhs = identity(witness)
    return lhs, rhs


def arrowchoice_left_composition_expr(
    witness: type[ArrowChoice[A, C]],
    f: ArrowChoice[A, B],
    g: ArrowChoice[B, C],
):
    """
    ArrowChoice law:
        left(g . f) == left(g) . left(f)
    """
    lhs = witness |left| (g |compose| f)
    rhs = (witness |left| g) |compose| (witness |left| f)
    return lhs, rhs


def arrowchoice_right_composition_expr(
    witness: type[ArrowChoice[A, C]],
    f: ArrowChoice[A, B],
    g: ArrowChoice[B, C],
):
    """
    ArrowChoice law:
        right(g . f) == right(g) . right(f)
    """
    lhs = witness |right| (g |compose| f)
    rhs = (witness |right| g) |compose| (witness |right| f)
    return lhs, rhs


def arrowchoice_split_choice_expr(
    witness: type[ArrowChoice[A, B]],
    value1: ArrowChoice[A, B],
    value2: ArrowChoice[C, D],
):
    """
    Derived ArrowChoice operation:
        f +++ g == left(f) >>> right(g)

    Expressed in (.) style:
        f +++ g == right(g) . left(f)
    """
    lhs = value1 |plusplus| (witness, value2)
    rhs = (witness |right| value2) |rcompose| (witness |left| value1)
    return lhs, rhs


def arrowchoice_fanin_expr(
    witness: type[ArrowChoice[A, C]],
    value1: ArrowChoice[A, C],
    value2: ArrowChoice[B, C],
):
    """
    Derived ArrowChoice operation:
        f ||| g == (f +++ g) >>> arr(merge)

    Expressed in (.) style:
        f ||| g == arr(merge) . (f +++ g)

    where:
        merge(Left(x))  = x
        merge(Right(y)) = y
    """
    def merge(either):
        return either.value

    lhs = value1 |oror| (witness, value2)
    rhs = (witness |arrow| merge) |compose| (value1 |plusplus| (witness, value2))
    return lhs, rhs
