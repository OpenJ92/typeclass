from typeclass.protocols.applicative import Applicative
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def assert_applicative_identity(v: Applicative[A], cls: type):
    """
    Identity Law:
        v.ap(cls.pure(lambda x: x)) == v

    Ensures that applying a pure identity function has no effect on the applicative value.

    Args:
        v: An Applicative instance.
        cls: The Applicative class constructor (e.g., Maybe).

    Raises:
        AssertionError: If the identity law fails.
    """
    assert v.ap(cls.pure(lambda x: x)) == v, "Applicative identity law failed"

def assert_applicative_homomorphism(cls: type, f: Callable[[A], B], x: A):
    """
    Homomorphism Law:
        cls.pure(x).ap(cls.pure(f)) == cls.pure(f(x))

    Ensures that applying a pure function to a pure value is the same as lifting the result.

    Args:
        cls: The Applicative class constructor.
        f: A function from A to B.
        x: A value of type A.

    Raises:
        AssertionError: If the homomorphism law fails.
    """
    assert cls.pure(x).ap(cls.pure(f)) == cls.pure(f(x)), "Applicative homomorphism law failed"

def assert_applicative_interchange(cls: type, u: Applicative[Callable[[A], B]], y: A):
    """
    Interchange Law:
        cls.pure(y).ap(u) == u.ap(cls.pure(lambda f: f(y)))

    Ensures function application is symmetric in the applicative structure.

    Args:
        cls: The Applicative class constructor.
        u: An Applicative containing a function.
        y: A value to apply.

    Raises:
        AssertionError: If the interchange law fails.
    """
    assert cls.pure(y).ap(u) == u.ap(cls.pure(lambda f: f(y))), "Applicative interchange law failed"

def assert_applicative_composition(cls: type, u: Applicative[Callable[[B], C]], v: Applicative[Callable[[A], B]], w: Applicative[A]):
    """
    Composition Law:
        cls.pure(lambda f: lambda g: lambda x: f(g(x))).ap(u).ap(v).ap(w) ==
        u.ap(v).ap(w)

    Ensures that function composition behaves correctly in the applicative context.

    Args:
        cls: The Applicative class constructor.
        u: An Applicative with a function from B to C.
        v: An Applicative with a function from A to B.
        w: An Applicative with a value of type A.

    Raises:
        AssertionError: If the composition law fails.
    """
    compose = lambda f: lambda g: lambda x: f(g(x))
    lhs = cls.pure(compose).ap(u).ap(v).ap(w)
    rhs = u.ap(v).ap(w)
    assert lhs == rhs, "Applicative composition law failed"

def assert_applicative_laws(cls: type, v: Applicative[A], f: Callable[[A], B], g: Callable[[B], C], x: A):
    """
    Runs all Applicative laws against a class and values.

    Args:
        cls: The Applicative class (e.g., Maybe).
        v: An Applicative instance of A.
        f: A function from A to B.
        g: A function from B to C.
        x: A plain value of type A.

    Raises:
        AssertionError: If any law fails.
    """
    # Compose for the composition test
    u = cls.pure(g)
    v_ = cls.pure(f)
    w = cls.pure(x)

    assert_applicative_identity(v, cls)
    assert_applicative_homomorphism(cls, f, x)
    assert_applicative_interchange(cls, cls.pure(f), x)
    assert_applicative_composition(cls, u, v_, w)

