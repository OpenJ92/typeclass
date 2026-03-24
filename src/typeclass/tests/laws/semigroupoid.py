from typing import TypeVar
from typeclass.typeclasses.semigroupoid import Semigroupoid
from typeclass.typeclasses.symbols import compose, rcompose

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


def semigroupoid_associativity_expr(f: Semigroupoid[A, B], g: Semigroupoid[B, C], h: Semigroupoid[C, D]):
    """
    Associativity law:
        (f >>> g) >>> h == f >>> (g >>> h)
    """
    lhs = (f |rcompose| g) |rcompose| h
    rhs = f |rcompose| (g |rcompose| h)
    return lhs, rhs


def semigroupoid_rassociativity_expr(f: Semigroupoid[A, B], g: Semigroupoid[B, C], h: Semigroupoid[C, D]):
    """
    Reverse composition associativity:
        h <<< (g <<< f) == (h <<< g) <<< f
    """
    lhs = h |compose| (g |compose| f)
    rhs = (h |compose| g) |compose| f
    return lhs, rhs


def semigroupoid_compose_rcompose_expr(f: Semigroupoid[A, B], g: Semigroupoid[B, C]):
    """
    Derived Semigroupoid operation:
        f >>> g == g <<< f
    """
    lhs = f |rcompose| g
    rhs = g |compose| f
    return lhs, rhs
