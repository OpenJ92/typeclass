from typeclass.protocols.functor import Functor
from typeclass.protocols.eq import Eq
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def assert_functor_identity(functor: Functor[A]):
    assert functor.fmap(lambda x: x) == functor, "Functor identity law failed"

def assert_functor_composition(functor: Functor[A], f: Callable[[A], B], g: Callable[[B], C]):
    assert functor.fmap(lambda x: g(f(x))) == functor.fmap(f).fmap(g), "Functor composition law failed"

def assert_functor_laws(functor: Functor[A], f: Callable[[A], B], g: Callable[[B], C]):
    assert_functor_identity(functor)
    assert_functor_composition(functor, f, g)

