from dataclasses import dataclass
from typing import TypeVar

from typeclass.typeclasses.category import Category
from typeclass.data.thunk import Thunk

A = TypeVar("A")
B = TypeVar("B")

@dataclass
class ID:
    cls: Thunk[type]

def identity(cls):
    """
    Identity morphism for a Category.

    Equivalent to `Category.identity(cls)`.

    Represents the categorical identity on `cls`. The identity
    morphism leaves values unchanged under composition.

    Identity must satisfy the unit laws:

        compose(fab, identity(A))
        ==
        fab

        compose(identity(B), fab)
        ==
        fab

    for any morphism `fab: A -> B`.

    Args:
        cls (type): The object (type) for which to construct
            the identity morphism.

    Returns:
        Category: The identity morphism on `cls`.
    """
    return ID(cls)
