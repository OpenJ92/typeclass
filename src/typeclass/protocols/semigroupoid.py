from typing import Protocol, runtime_checkable, Self


@runtime_checkable
class Semigroupoid(Protocol):
    """
    Semigroupoid typeclass.

    A Semigroupoid supports associative composition of morphisms, but does not
    necessarily have an identity morphism.

    Core operation:
        compose : (b -> c) -> (a -> b) -> (a -> c)

    Laws:
        Associativity:
            (h ∘ g) ∘ f == h ∘ (g ∘ f)

    Notes:
        - Unlike Semigroup, Semigroupoid is about composing *arrows/morphisms*.
        - In many codebases you'll also expose a flipped version ("then"):
              f.then(g) == g.compose(f)
          but the only required op here is `compose`.
    """

    def compose(self, other: Self) -> Self:
        """
        Compose this morphism after `other`.

        Interpreting `other` as f : a -> b and `self` as g : b -> c,
        `self.compose(other)` should represent g ∘ f : a -> c.

        Returns:
            Self: the composed morphism.

        Must be associative.
        """
        ...
