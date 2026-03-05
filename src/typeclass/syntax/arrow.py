from dataclasses import dataclass
from typing import TypeVar

from typeclass.protocols.arrow import Arrow
from typeclass.data.thunk import Thunk

@dataclass
class Arr:
    cls: type
    fab: Thunk[Callable[[A], B]]

@dataclass
class First:
    aab: Thunk[Arrow[A, B]]

@dataclass
class Second:
    aab: Thunk[Arrow[A, B]]

@dataclass
class Split:
    aab: Thunk[Arrow[A, B]]
    acd: Thunk[Arrow[C, D]]

@dataclass
class Fanout:
    aab: Thunk[Arrow[A, B]]
    acd: Thunk[Arrow[C, D]]

def arrow(cls, fab):
    """
    Lift a function into an Arrow.

    Equivalent to `Arrow.arrow(cls, fab)`.

    Constructs an arrow from a pure function. This operation embeds
    ordinary computation into the Arrow context.

    The lifted function behaves like the underlying function under
    composition and must satisfy the Arrow laws:

        arrow(id)
        ==
        identity

        arrow(f >>> g)
        ==
        compose(arrow(f), arrow(g))

    where `f` and `g` are ordinary functions.

    Args:
        cls (type): The Arrow implementation in which the function
            should be lifted.
        fab (Callable[[A], B]): A pure function from `A` to `B`.

    Returns:
        Arrow: An arrow representing the lifted function `A -> B`.
    """
    return Arr(cls, Thunk(lambda: fab))

def first(aab):
    """
    Lift a function into an Arrow.

    Equivalent to `Arrow.arrow(cls, fab)`.

    Constructs an arrow from a pure function. This operation embeds
    ordinary computation into the Arrow context.

    The lifted function behaves like the underlying function under
    composition and must satisfy the Arrow laws:

        arrow(id)
        ==
        identity

        arrow(f >>> g)
        ==
        compose(arrow(f), arrow(g))

    where `f` and `g` are ordinary functions.

    Args:
        cls (type): The Arrow implementation in which the function
            should be lifted.
        fab (Callable[[A], B]): A pure function from `A` to `B`.

    Returns:
        Arrow: An arrow representing the lifted function `A -> B`.
    """
    return First(Thunk(lambda: aab))

def second(aab):
    """
    Apply an ArrowChoice to the `Right` branch of an Either.

    Equivalent to `aab.right()`.

    Constructs an arrow which runs `aab` on values wrapped in `Right`,
    leaving `Left` values untouched.

    Given:

        aab : A -> B

    the resulting arrow has type:

        Either[C, A] -> Either[C, B]

    This operation is symmetric to `left`, but applies the arrow to the
    `Right` branch instead of the `Left` branch.

    In the syntax layer this is represented as an intent node. The
    interpreter lowers it using `left` together with `arr`-lifted
    swapping of the Either branches.

    Args:
        aab (ArrowChoice[A, B]): Arrow applied to the Right branch.

    Returns:
        ArrowChoice: An intent node representing `right aab`.
    """
    return Second(Thunk(lambda: aab))

def split(aab, acd):
    """
    Parallel composition of two Arrows.

    Equivalent to `aab *** acd`.

    Constructs an arrow which applies two independent arrows to
    the components of a pair.

    Given:

        aab : A -> B
        acd : C -> D

    the resulting arrow has type:

        (A, C) -> (B, D)

    Each component of the pair is processed independently by the
    corresponding arrow.

    Args:
        aab (Arrow[A, B]): Arrow operating on the first component.
        acd (Arrow[C, D]): Arrow operating on the second component.

    Returns:
        Arrow: An arrow mapping `(A, C)` to `(B, D)` by applying
        each arrow to its corresponding component.
    """
    return Split(Thunk(lambda: aab), Thunk(lambda: acd))

def fanout(aab, aac):
    """
    Fanout composition of two Arrows.

    Equivalent to `aab &&& acd`.

    Constructs an arrow which applies two arrows to the same input
    and returns both results as a pair.

    Given:

        aab : A -> B
        acd : A -> C

    the resulting arrow has type:

        A -> (B, C)

    This operation duplicates the input so both arrows may operate
    on the same value.

    Args:
        aab (Arrow[A, B]): First arrow applied to the input.
        acd (Arrow[A, C]): Second arrow applied to the same input.

    Returns:
        Arrow: An arrow mapping `A` to `(B, C)` containing both results.
    """
    return Fanout(Thunk(lambda: aab), Thunk(lambda: aac))
