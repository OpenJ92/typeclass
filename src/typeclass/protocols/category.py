from typing import Protocol, runtime_checkable, Self

from typeclass.protocols.semigroupoid import Semigroupoid


@runtime_checkable
class Category(Semigroupoid, Protocol):
    """
    Category typeclass.

    A Category is a Semigroupoid with an identity morphism.

    Core operations:
        compose : (b -> c) -> (a -> b) -> (a -> c)
        id      : a -> a

    Laws:
        Associativity:
            (h ∘ g) ∘ f == h ∘ (g ∘ f)

        Left identity:
            id ∘ f == f

        Right identity:
            f ∘ id == f
    """

    @classmethod
    def id(cls) -> Self:
        """
        Return the identity morphism for this category.

        Must satisfy:
            cls.id().compose(f) == f
            f.compose(cls.id()) == f
        """
        ...
