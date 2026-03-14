from dataclasses import dataclass
from typing import TypeVar

from typeclass.data.thunk import Thunk
from typeclass.protocols.comonad import Comonad
from typeclass.syntax.functor import fmap

A = TypeVar("A")
B = TypeVar("B")

@dataclass
class Extract:
    wa: Thunk[Comonad[A]]


@dataclass
class Duplicate:
    wa: Thunk[Comonad[A]]


def extract(wa: Comonad[A]):
    """
    Retrieve the focused value from a comonadic context.

    This is the standalone syntax constructor for `wa.extract()`.

    Args:
        wa: A comonadic value containing a focused value of type A.

    Returns:
        A syntax node representing extraction of the focused value.
    """
    return Extract(Thunk(lambda: wa))


def duplicate(wa: Comonad[A]) -> Comonad[Comonad[A]]:
    """
    Duplicate a comonadic context so that each position contains
    its own local sub-context.

    This is the standalone syntax constructor for `wa.duplicate()`.

    Args:
        wa: A comonadic value.

    Returns:
        A syntax node representing duplication of the comonadic context.
    """
    return Duplicate(Thunk(lambda: wa))

def extend(wa: Comonad[A], f: Callable[[Comonad[A]], B]):
    """
    Transform a comonadic structure by applying a function
    to every local context.

    This is the standalone derived combinator for Comonad:

        extend f == fmap f . duplicate

    Args:
        f: A function from a comonadic context to a value.
        wa: A comonadic value.

    Returns:
        A syntax expression equivalent to `fmap(f, duplicate(wa))`.
    """
    return fmap(duplicate(wa), f)
