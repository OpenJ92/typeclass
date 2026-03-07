from dataclasses import dataclass
from typing import TypeVar

from typeclass.protocols.arrowchoice import ArrowChoice
from typeclass.data.thunk import Thunk

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


@dataclass
class Left:
    cls: type
    aab: Thunk[ArrowChoice[A, B]]

@dataclass
class Right:
    cls: type
    aab: Thunk[ArrowChoice[A, B]]


@dataclass
class PlusPlus:
    cls: type
    aab: Thunk[ArrowChoice[A, B]]
    acd: Thunk[ArrowChoice[C, D]]


@dataclass
class OrOr:
    cls: type
    aab: Thunk[ArrowChoice[A, B]]
    acb: Thunk[ArrowChoice[C, B]]


def left(cls, aab):
    """
    Apply an ArrowChoice to the `Left` branch of an Either.

    Equivalent to `aab.left()`.

    Constructs an arrow which runs `aab` on values wrapped in `Left`,
    leaving `Right` values untouched.

    Given:

        aab : A -> B

    the resulting arrow has type:

        Either[A, C] -> Either[B, C]

    This is the single required primitive for ArrowChoice; other
    ArrowChoice combinators can be represented as intent nodes and
    lowered by the interpreter.

    Args:
        aab (ArrowChoice[A, B]): Arrow applied to the Left branch.

    Returns:
        ArrowChoice: An intent node representing `left aab`.
    """
    return Left(cls, Thunk(lambda: aab))

def right(cls, aab):
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
    return Right(cls, Thunk(lambda: aab))


def plusplus(aab, clsacd):
    """
    Route over Either in parallel (written `+++`).

    Constructs an arrow which applies one arrow to `Left` values and
    another arrow to `Right` values.

    Given:

        aab : A -> B
        acd : C -> D

    the resulting arrow has type:

        Either[A, C] -> Either[B, D]

    This is an intent node. The interpreter lowers it using `left`
    (and Arrow structure), rather than desugaring it here.

    Args:
        aab (ArrowChoice[A, B]): Arrow applied to the Left branch.
        acd (ArrowChoice[C, D]): Arrow applied to the Right branch.

    Returns:
        ArrowChoice: An intent node representing `aab +++ acd`.
    """
    cls, acd = clsacd
    return PlusPlus(cls, Thunk(lambda: aab), Thunk(lambda: acd))


def oror(aab, clsacb):
    """
    Fan-in / case analysis over Either (written `|||`), named `oror`.

    Constructs an arrow which chooses between two arrows based on
    whether the input is `Left` or `Right`, producing a single output.

    Given:

        aab : A -> B
        acb : C -> B

    the resulting arrow has type:

        Either[A, C] -> B

    This is an intent node. The interpreter lowers it in terms of
    `plusplus` and an `arr`-lifted merge.

    Args:
        aab (ArrowChoice[A, B]): Arrow used when input is `Left(a)`.
        acb (ArrowChoice[C, B]): Arrow used when input is `Right(c)`.

    Returns:
        ArrowChoice: An intent node representing `aab ||| acb`.
    """
    cls, acb = clsacb
    return OrOr(cls, Thunk(lambda: aab), Thunk(lambda: acb))
