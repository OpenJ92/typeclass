from typeclass.protocols.functor import Functor
from typeclass.protocols.eq import Eq
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def assert_functor_identity(functor: Functor[A]):
    """
    Identity Law:
        fa.fmap(lambda x: x) == fa

    Ensures that mapping the identity function over a functor returns the same functor.

    Args:
        fa: A Functor instance.

    Raises:
        AssertionError: If the identity law fails.
    """
    assert functor.fmap(lambda x: x) == functor, "Functor identity law failed"

def assert_functor_composition(functor: Functor[A], f: Callable[[A], B], g: Callable[[B], C]):
    """
    Composition Law:
        fa.fmap(lambda x: g(f(x))) == fa.fmap(f).fmap(g)

    Ensures that mapping a composed function is equivalent to mapping in sequence.

    Args:
        fa: A Functor instance.
        f: A function from A to B.
        g: A function from B to C.

    Raises:
        AssertionError: If the composition law fails.
    """
    assert functor.fmap(lambda x: g(f(x))) == functor.fmap(f).fmap(g), "Functor composition law failed"

def assert_functor_laws(functor: Functor[A], f: Callable[[A], B], g: Callable[[B], C]):
    """
    Runs all Functor laws on the given instance and functions.

    Args:
        fa: A Functor instance.
        f: A function from A to B.
        g: A function from B to C.

    Raises:
        AssertionError: If any law fails.
    """
    assert_functor_identity(functor)
    assert_functor_composition(functor, f, g)

