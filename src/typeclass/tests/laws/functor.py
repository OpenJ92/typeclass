from typing import Callable, TypeVar
from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.symbols import fmap, replace, void

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def functor_identity_expr(functor: Functor[A]):
    """
    Identity law:
        fmap id == id
    """
    lhs = functor |fmap| (lambda x: x)
    rhs = functor
    return lhs, rhs


def functor_composition_expr(
    functor: Functor[A],
    f: Callable[[A], B],
    g: Callable[[B], C],
):
    """
    Composition law:
        fmap (g . f) == fmap f . fmap g
    """
    lhs = functor |fmap| (lambda x: g(f(x)))
    rhs = functor |fmap| f |fmap| g
    return lhs, rhs


def functor_replace_expr(functor: Functor[A], value: B):
    """
    Derived Functor operation:
        replace(value, fa) == fmap(lambda _: value, fa)
    """
    lhs = value |replace| functor
    rhs = functor |fmap| (lambda _: value)
    return lhs, rhs


def functor_void_expr(functor: Functor[A]):
    """
    Derived Functor operation:
        void(fa) == fmap(lambda _: None, fa)
    """
    lhs = void(functor)
    rhs = functor |fmap| (lambda _: None)
    return lhs, rhs
