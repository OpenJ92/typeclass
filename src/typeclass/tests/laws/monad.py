from typeclass.protocols.monad import Monad
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def assert_monad_left_identity(cls: type, a: A, f: Callable[[A], Monad[B]]):
    """
    Left Identity Law:
        return a >>= f == f a

    Ensures that embedding a value into the monadic context and then binding
    is the same as applying the function directly.

    Args:
        cls: The Monad class constructor (e.g., Maybe).
        a: A plain value of type A.
        f: A function from A to Monad[B].

    Raises:
        AssertionError: If the left identity law fails.
    """
    assert cls.return_(a).bind(f) == f(a), "Monad left identity law failed"


def assert_monad_right_identity(m: Monad[A], cls: type):
    """
    Right Identity Law:
        m >>= return == m

    Ensures that binding a monadic value with `return_` does not change it.

    Args:
        m: A Monad instance.
        cls: The Monad class constructor (e.g., Maybe).

    Raises:
        AssertionError: If the right identity law fails.
    """
    assert m.bind(cls.return_) == m, "Monad right identity law failed"


def assert_monad_associativity(m: Monad[A], f: Callable[[A], Monad[B]], g: Callable[[B], Monad[C]]):
    """
    Associativity Law:
        (m >>= f) >>= g == m >>= (lambda x: f x >>= g)

    Ensures that the grouping of sequential binds does not affect the result.

    Args:
        m: A Monad instance.
        f: A function from A to Monad[B].
        g: A function from B to Monad[C].

    Raises:
        AssertionError: If the associativity law fails.
    """
    left = m.bind(f).bind(g)
    right = m.bind(lambda x: f(x).bind(g))
    assert left == right, "Monad associativity law failed"


def assert_monad_laws(
        cls: type,
        m: Monad[A],
        a: A,
        f: Callable[[A], Monad[B]],
        g: Callable[[B], Monad[C]],
    ):
    """
    Runs all Monad laws against a class and values.

    Args:
        cls: The Monad class (e.g., Maybe).
        m: A Monad instance of A.
        a: A plain value of type A.
        f: A function from A to Monad[B].
        g: A function from B to Monad[C].

    Raises:
        AssertionError: If any law fails.
    """
    assert_monad_left_identity(cls, a, f)
    assert_monad_right_identity(m, cls)
    assert_monad_associativity(m, f, g)
