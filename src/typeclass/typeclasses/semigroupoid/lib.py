from dataclasses import dataclass

from typing import Protocol, TypeVar, runtime_checkable, Self

from typeclass.typeclasses.semigroupoid import Semigroupoid
from typeclass.data.thunk import Thunk

A = TypeVar("A")
B = TypeVar("B")

@dataclass
class Compose:
    fbc: Thunk[Semigroupoid]
    fab: Thunk[Semigroupoid]


def compose(fbc: Semigroupoid, fab: Semigroupoid):
    """
    Compose two Semigroupoid values.

    Equivalent to `fbc.compose(fab)` or `fbc ∘ fab`.

    Represents categorical composition: apply `fab` first,
    then `fbc`.

    Composition must be associative:

        compose(fcd, compose(fbc, fab))
        ==
        compose(compose(fcd, fbc), fab)

    Args:
        fbc (Semigroupoid): A morphism from B to C.
        fab (Semigroupoid): A morphism from A to B.

    Returns:
        Semigroupoid: The composed morphism from A to C.
    """
    return Compose(Thunk(lambda: fbc), Thunk(lambda: fab))

def rcompose(fab: Semigroupoid, fbc: Semigroupoid):
    """
    Reverse composition of two Semigroupoid values.

    Equivalent to `fab.rcompose(fbc)` and defined as:

        rcompose(fab, fbc) == compose(fbc, fab)

    Represents forward composition: apply `fab` first,
    then `fbc`.

    Reverse composition is associative, inherited from
    categorical composition:

        rcompose(rcompose(fab, fbc), fcd)
        ==
        rcompose(fab, rcompose(fbc, fcd))

    Args:
        fab (Semigroupoid): A morphism from A to B.
        fbc (Semigroupoid): A morphism from B to C.

    Returns:
        Semigroupoid: The composed morphism from A to C.
    """
    return compose(fbc, fab)
