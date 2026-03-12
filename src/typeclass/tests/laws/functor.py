from typeclass.protocols.functor import Functor
from typeclass.interpret.interpreter import interpret
from typeclass.syntax.symbols import fmap, replace, void
from typing import Callable, TypeVar, Any

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def assert_functor_identity(functor: Functor[A]):
    """
    Identity Law:
        fmap id == id

    Ensures that mapping the identity function over a functor returns the same functor.

    Args:
        fa: A Functor instance.

    Raises:
        AssertionError: If the identity law fails.
    """
    lhs = functor |fmap| (lambda x: x)
    rhs = functor
    assert interpret(lhs, None, None).force() == interpret(rhs, None, None).force(), "Functor identity law failed"

def assert_functor_composition(functor: Functor[A], f: Callable[[A], B], g: Callable[[B], C]):
    """
    Composition Law:
        fmap (f . g) == fmap f . fmap g

    Ensures that mapping a composed function is equivalent to mapping in sequence.

    Args:
        fa: A Functor instance.
        f: A function from A to B.
        g: A function from B to C.

    Raises:
        AssertionError: If the composition law fails.
    """
    lhs = functor |fmap| (lambda x: g(f(x)))
    rhs = functor |fmap| f |fmap| g
    assert interpret(lhs, None, None).force() == interpret(rhs, None, None).force(), "Functor composition law failed"

def assert_functor_replace(functor: Any, value: B) -> None:
    """
    Assert that `replace` agrees with its canonical Functor definition.

    For any Functor value `fa` and replacement value `b`,
    replacing every element of `fa` with `b` should be equivalent to
    mapping the constant function `lambda _: b` over `fa`.

        replace(b, fa) == fmap(lambda _: b, fa)

    This assertion is checked through the DSL surface and interpreter,
    not by calling the underlying implementation methods directly.
    """
    lhs = value |replace| functor
    rhs = functor |fmap| (lambda _: value)

    assert interpret(lhs, None, None).force() == interpret(rhs, None, None).force()

def assert_functor_void(functor: Any) -> None:
    """
    Assert that `void` agrees with its canonical Functor definition.

    For any Functor value `fa`, voiding `fa` should be equivalent to
    mapping a constant `None` over `fa`.

        void(fa) == fmap(lambda _: None, fa)

    This assertion is checked through the DSL surface and interpreter,
    not by calling the underlying implementation methods directly.
    """
    lhs = void(functor)
    rhs = functor |fmap| (lambda _: None)

    assert interpret(lhs, None, None).force() == interpret(rhs, None, None).force()

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

def assert_functor_derived(functor: Any, value: B) -> None:
    """
    Assert that the Functor-derived operations `replace` and `void`
    satisfy their canonical definitions.
    """
    assert_functor_replace(functor, value)
    assert_functor_void(functor)
