from typing import Callable, TypeVar
from typeclass.protocols.applicative import Applicative
from typeclass.syntax.symbols import fmap, pure, ap, then, skip, liftA2

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def applicative_identity_expr(cls: type, value: Applicative[A]):
    """
    Identity law:
        pure id <*> v == v
    """
    lhs = cls |pure| (lambda x: x) |ap| value
    rhs = value
    return lhs, rhs


def applicative_homomorphism_expr(cls: type, f: Callable[[A], B], x: A):
    """
    Homomorphism law:
        pure f <*> pure x == pure (f x)
    """
    lhs = cls |pure| f |ap| (cls |pure| x)
    rhs = cls |pure| f(x)
    return lhs, rhs


def applicative_interchange_expr(cls: type, u: Applicative[Callable[[A], B]], y: A):
    """
    Interchange law:
        u <*> pure y == pure ($ y) <*> u
    """
    lhs = u |ap| (cls |pure| y)
    rhs = cls |pure| (lambda f: f(y)) |ap| u
    return lhs, rhs


def applicative_composition_expr(
    cls: type,
    u: Applicative[Callable[[B], C]],
    v: Applicative[Callable[[A], B]],
    w: Applicative[A],
):
    """
    Composition law:
        pure (.) <*> u <*> v <*> w == u <*> (v <*> w)
    """
    compose = lambda f: lambda g: lambda x: f(g(x))
    lhs = cls |pure| compose |ap| u |ap| v |ap| w
    rhs = u |ap| (v |ap| w)
    return lhs, rhs


def applicative_then_expr(fa: Applicative[A], fb: Applicative[B]):
    """
    Derived Applicative operation:
        then(fa, fb) == liftA2(lambda _, b: b, fa, fb)
    """
    lhs = fa |then| fb
    rhs = liftA2(lambda _, b: b, fa, fb)
    return lhs, rhs


def applicative_skip_expr(fa: Applicative[A], fb: Applicative[B]):
    """
    Derived Applicative operation:
        skip(fa, fb) == liftA2(lambda a, _: a, fa, fb)
    """
    lhs = fa |skip| fb
    rhs = liftA2(lambda a, _: a, fa, fb)
    return lhs, rhs


def applicative_liftA2_expr(
    f: Callable[[A, B], C],
    fa: Applicative[A],
    fb: Applicative[B],
):
    """
    Derived Applicative operation:
        liftA2(f, fa, fb) == fmap(fa, lambda a: lambda b: f(a, b)) <*> fb
    """
    lhs = liftA2(f, fa, fb)
    rhs = (fa |fmap| (lambda a: lambda b: f(a, b))) |ap| fb
    return lhs, rhs
