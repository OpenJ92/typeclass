from __future__ import annotations

from typing import Protocol, Callable, TypeVar, Generic, runtime_checkable, Self

from typeclass.protocols.category import Category
from typeclass.protocols.force import Force

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


@runtime_checkable
class Arrow(Category, Protocol, Generic[A, B]):
    """
    Arrow typeclass.

    An Arrow is a Category with additional structure for building *structured*
    computations: not just sequential composition, but also “wiring” that
    interacts with products (pairs).

    This is the abstraction you were reaching for when you tried to use
    Applicative as a way to represent computation structure (and even potential
    parallel structure) inside the AST. Applicative is great for *combining*
    independent results inside a context, but Arrow is the native home for
    explicit dataflow / wiring combinators:
      - lift a pure function into an arrow (`arr`)
      - run an arrow on the left side of a pair (`first`)
      - derive parallel product composition (`***`)
      - derive fanout / duplication (`&&&`)

    Why it clicked:

    - With your AST-based design, you want to represent computation as a graph
      you can *walk*, *rewrite*, and (eventually) *schedule*. You already do
      this for sequential structure via `compose` (Semigroupoid/Category).
      :contentReference[oaicite:1]{index=1}

    - Applicative gives a way to combine effects, but it doesn’t directly give
      the “wiring primitives” that make graphs explicit (pairs, fanout, routing).
      Arrow *does*.

    - Once Arrow combinators exist as syntax nodes, you can identify subtrees
      that correspond to independent computation (e.g. `f *** g *** h ...`) and
      rewrite them into a normalized n-ary “parallel bundle” node, then choose
      an execution backend (sequential, threadpool, processpool, etc.) without
      changing the surface language.

    Fanout (&&&):

    - Fanout duplicates the same input into two arrows and pairs their results.

          (f &&& g) : a -> (b, c)
          (f &&& g)(x) = (f(x), g(x))

      This is the “graph” combinator: it turns one stream of data into two
      parallel branches. When combined with `***` and `compose`, this is enough
      to build DAG-shaped computations.

    Core operations:
        arr   : (a -> b) -> arr a b
        first : arr a b  -> arr (a, c) (b, c)

    Derived operations (recommended helpers, definable from the core):
        second : arr a b -> arr (c, a) (c, b)
        (***)  : arr a b -> arr c d -> arr (a, c) (b, d)
        (&&&)  : arr a b -> arr a c -> arr a (b, c)

    Laws (typical Arrow laws; stated informally):
        - arr preserves identity and composition (a functor from (->) to arr):
              arr(id) == id
              arr(g ∘ f) == arr(g) ∘ arr(f)

        - first respects identity and composition:
              first(id) == id
              first(g ∘ f) == first(g) ∘ first(f)

        - coherence with pairing/associativity (for real implementations):
          product reassociation and projections behave as expected.
          (In Python you’ll likely pick a canonical tuple nesting.)
    """

    @classmethod
    def arrow(cls, f: Force[Callable[[A], B]]) -> Arrow[A, B]:
        """
        Lift a pure function into the Arrow.

        Equivalent to embedding (->) into the Arrow.

        Must satisfy:
            cls.arrow(lambda x: x) == cls.id()
            cls.arrow(g).compose(cls.arrow(f)) == cls.arrow(lambda x: g(f(x)))

        Args:
            f (Callable[[A], B]): A pure function.

        Returns:
            Arrow[A, B]: The lifted arrow.
        """
        ...


    @classmethod
    def first(cls, self: Force[Arrow[A, B]]) -> Arrow[tuple[A, C], tuple[B, C]]:
        """
        Apply this Arrow to the first component of a pair, leaving the second
        component unchanged.

            first(f)(a, c) == (f(a), c)

        Must satisfy:
            cls.first(id) == id
            cls.first(g ∘ f) == cls.first(g) ∘ cls.first(f)

        Returns:
            Arrow[tuple[A, C], tuple[B, C]]: The lifted arrow on pairs.
        """
        ...
