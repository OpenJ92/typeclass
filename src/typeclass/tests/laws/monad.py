from typing import Callable, TypeVar
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.symbols import pure, bind, mthen, join, rbind, kleisli, rkleisli

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def monad_left_identity_expr(cls: type, x: A, f: Callable[[A], Monad[B]]):
    """
    Left identity:
        return x >>= f == f x
    """
    lhs = cls |pure| x |bind| f
    rhs = f(x)
    return lhs, rhs


def monad_right_identity_expr(value: Monad[A], cls: type):
    """
    Right identity:
        m >>= return == m
    """
    lhs = value |bind| (lambda x: cls |pure| x)
    rhs = value
    return lhs, rhs


def monad_associativity_expr(
    value: Monad[A],
    f: Callable[[A], Monad[B]],
    g: Callable[[B], Monad[C]],
):
    """
    Associativity:
        (m >>= f) >>= g == m >>= (lambda x: f x >>= g)
    """
    lhs = (value |bind| f) |bind| g
    rhs = value |bind| (lambda x: f(x) |bind| g)
    return lhs, rhs


def monad_join_expr(value: Monad[Monad[A]]):
    """
    Derived Monad operation:
        join(mma) == mma >>= id
    """
    lhs = join(value)
    rhs = value |bind| (lambda x: x)
    return lhs, rhs


def monad_mthen_expr(ma: Monad[A], mb: Monad[B]):
    """
    Derived Monad operation:
        ma >> mb == ma >>= (lambda _: mb)
    """
    lhs = ma |mthen| mb
    rhs = ma |bind| (lambda _: mb)
    return lhs, rhs


def monad_rbind_expr(f: Callable[[A], Monad[B]], ma: Monad[A]):
    """
    Derived Monad operation:
        f =<< ma == ma >>= f
    """
    lhs = f |rbind| ma
    rhs = ma |bind| f
    return lhs, rhs


def monad_kleisli_expr(
    f: Callable[[A], Monad[B]],
    g: Callable[[B], Monad[C]],
    x: A,
):
    """
    Derived Monad operation:
        (f >=> g)(x) == f(x) >>= g
    """
    lhs = (f |kleisli| g)(x)
    rhs = f(x) |bind| g
    return lhs, rhs


def monad_rkleisli_expr(
    f: Callable[[A], Monad[B]],
    g: Callable[[B], Monad[C]],
    x: A,
):
    """
    Derived Monad operation:
        (g <=< f)(x) == f(x) >>= g
    """
    lhs = (f |rkleisli| g)(x)
    rhs = g(x) |bind| f
    return lhs, rhs
