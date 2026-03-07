from dataclasses import dataclass
from typing import TypeVar

from typeclass.protocols.arrowapply import ArrowApply
from typeclass.data.thunk import Thunk

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

@dataclass
class Apply:
    cls: type

def apply(cls):
    """
    Dynamically apply an Arrow to an input.

    Equivalent to `ArrowApply.app(cls)`.

    Constructs an arrow which takes a pair consisting of an arrow
    and an input for that arrow, and applies the arrow to the input.

    Given:

        (arr A B, A)

    the resulting arrow has type:

        (arr A B, A) -> B

    This operation enables dynamic arrow application: the arrow to be
    executed may itself be produced by a prior computation.

    `app` is the primitive operation of the ArrowApply typeclass. It
    extends the Arrow interface with the ability to treat arrows as
    first-class values that may be passed around and applied at runtime.

    Args:
        cls (type): The ArrowApply implementation providing the
            `app` primitive.

    Returns:
        ArrowApply: An arrow which applies a supplied arrow to
        its corresponding input.
    """
    return Apply(cls)
