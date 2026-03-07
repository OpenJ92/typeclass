# src/typeclass/protocols/arrow_choice.py
from __future__ import annotations

from typing import Protocol, TypeVar, Generic, runtime_checkable

from typeclass.protocols.arrow import Arrow
from typeclass.data.either import Either, Left, Right

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


@runtime_checkable
class ArrowChoice(Arrow[A, B], Protocol, Generic[A, B]):
    """
    ArrowChoice typeclass.

    ArrowChoice extends Arrow with *sum* (coproduct) structure, enabling
    branching / routing based on an Either input.

    If `Either[a, c]` is your coproduct, ArrowChoice gives you the ability to:
      - run an arrow only when input is Left, passing Right through unchanged
      - run an arrow only when input is Right, passing Left through unchanged
      - combine two arrows to handle Left/Right cases (choice / case analysis)

    This is the natural companion to Arrow's product structure (pairs):
      - Arrow gives wiring over tuples (products)
      - ArrowChoice gives wiring over Either (coproducts)

    Core operations (common minimal basis):
        left  : arr a b -> arr (Either a c) (Either b c)
        right : arr a b -> arr (Either c a) (Either c b)

    Typical derived operations:
        split_choice (often written +++):
            f +++ g : Either a c -> Either b d
            - apply f to Left(a)
            - apply g to Right(c)

        fanin (often written |||):
            f ||| g : Either a c -> b
            - apply f to Left(a)
            - apply g to Right(c)
            (requires same output type)

    Laws (informal; implementations should satisfy the usual ArrowChoice laws):

    - Naturality / coherence for `left`:
        left(arr(f)) == arr(map_left(f))
        where map_left(f)(Left(x))  = Left(f(x))
              map_left(f)(Right(y)) = Right(y)

    - Identity:
        left(id) == id
        right(id) == id

    - Composition:
        left(g ∘ f) == left(g) ∘ left(f)
        right(g ∘ f) == right(g) ∘ right(f)

    - Coherence with Arrow `first` / products (for “real” instances):
        various distributivity/associativity laws relating pair structure and
        Either structure, depending on the chosen canonical representations.

    Notes for your AST/syntax setup:
      - `left` / `right` are the crucial intent nodes. Once you have them,
        you can build higher-level combinators (like `split_choice` / `fanin`)
        as nodes or as derived helpers.
      - With `Either`, you can represent conditional routing in a DAG without
        “executing” the branch in the syntax: the interpreter chooses based on
        the runtime tag (Left/Right).
    """

    @classmethod
    def left(cls, self: ArrowChoice[A, B]) -> ArrowChoice[Either[A, C], Either[B, C]]:
        """
        Route this arrow down the Left branch of an Either.

            left(f)(Left(a))   == Left(f(a))
            left(f)(Right(c))  == Right(c)

        Returns:
            ArrowChoice[Either[A, C], Either[B, C]]
        """
        ...
