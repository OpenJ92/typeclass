from typing import TypeVar
from typeclass.protocols.semigroupoid import Semigroupoid
from typeclass.syntax.symbols import compose, rcompose

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


def semigroupoid_associativity_expr(f: Semigroupoid[A, B], g: Semigroupoid[B, C], h: Semigroupoid[C, D]):
    """
    Associativity law:
        (f >>> g) >>> h == f >>> (g >>> h)
    """
    lhs = (f |compose| g) |compose| h
    rhs = f |compose| (g |compose| h)
    return lhs, rhs


def semigroupoid_rassociativity_expr(f: Semigroupoid[A, B], g: Semigroupoid[B, C], h: Semigroupoid[C, D]):
    """
    Reverse composition associativity:
        h <<< (g <<< f) == (h <<< g) <<< f
    """
    lhs = h |rcompose| (g |rcompose| f)
    rhs = (h |rcompose| g) |rcompose| f
    return lhs, rhs


def semigroupoid_compose_rcompose_expr(f: Semigroupoid[A, B], g: Semigroupoid[B, C]):
    """
    Derived Semigroupoid operation:
        f >>> g == g <<< f
    """
    lhs = f |compose| g
    rhs = g |rcompose| f
    return lhs, rhs
