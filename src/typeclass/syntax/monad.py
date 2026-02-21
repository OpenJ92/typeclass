from dataclasses import dataclass
from typeing import Typevar, Callable

from typeclass.data.thunk import Thunk
from typeclass.protocols.monad import Monad

A = Typevar("A")
B = Typevar("B")

@dataclass
class Return:
    cls: type
    value: Thunk

@dataclass
class Bind:
    ma: Thunk
    f: Thunk

def return_(cls: type, value: A) -> Monad[A]:
    """
    Embed a raw value into the monadic context.

    This is the standalone version of `Monad.return_(value)`,
    matching Haskell's `return` (and equivalent to `pure`).

    Args:
        cls: The Monad type into which the value should be embedded.
        value: A raw value of type A.

    Returns:
        A Monad containing the provided value.
    """
    return Return(cls, Thunk(lambda: value))

def bind(ma: Monad[A], f: Callable[[A],Monad[B]]) -> Monad[B]:
    """
    Sequence a monadic computation by applying a function to the wrapped value,
    where the function itself returns a new monadic context.

    This is the standalone version of `ma.bind(f)`, matching Haskell's `>>=`.

    Args:
        ma: A Monad containing a value of type A.
        f: A function that takes a value of type A and returns a Monad of type B.

    Returns:
        A Monad representing the result of applying the function to the unwrapped value
        and flattening the resulting monadic structure.
    """
    return Bind(Thunk(lambda: ma), Thunk(lambda: f))

def then(ma: Monad[A], mb: Monad[B]) -> Monad[B]:
    """
    Sequence two monadic computations, discarding the result of the first.

    This is the standalone version of `ma >> mb`, matching Haskell's `(>>)`.

    Args:
        ma: A Monad representing the first computation.
        mb: A Monad representing the second computation.

    Returns:
        A Monad representing the sequential execution of `ma` followed by `mb`,
        where the value produced by `ma` is ignored.
    """
    return bind(ma, lambda _: mb)

def join(mma: Monad[Monad[A]]) -> Monad[A]:
    """
    Flatten a nested monadic computation.

    This matches Haskell's `join`.

    Args:
        mma: A Monad containing another Monad.

    Returns:
        A Monad with one level of monadic structure removed.
    """
    return bind(mma, lambda ma: ma)

def bind_flipped(f: Callable[[A], Monad[B]], ma: Monad[A]) -> Monad[B]:
    """
    Apply a monadic function to a monadic value (flipped bind).

    This matches Haskell's `(=<<)`.

    Args:
        f: A function from A to Monad[B].
        ma: A Monad containing a value of type A.

    Returns:
        The result of sequencing `ma` into `f`.
    """
    return bind(ma, f)

def kleisli(f: Callable[[A], Monad[B]], g: Callable[[B], Monad[C]]) -> Callable[[A], Monad[C]]:
    """
    Compose two monadic functions.

    This matches Haskell's `(>=>)`.

    Args:
        f: A function from A to Monad[B].
        g: A function from B to Monad[C].

    Returns:
        A function h such that:
            h(a) = f(a) >>= g
    """
    return lambda a: bind(f(a), g)

def kleisli_rev(g: Callable[[B], Monad[C]],
                f: Callable[[A], Monad[B]]) -> Callable[[A], Monad[C]]:
    """
    Compose two monadic functions (reverse order).

    This matches Haskell's `(<=<)`.

    Args:
        g: A function from B to Monad[C].
        f: A function from A to Monad[B].

    Returns:
        A function h such that:
            h(a) = f(a) >>= g
    """
    return lambda a: bind(f(a), g)
