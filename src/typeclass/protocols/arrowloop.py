# src/typeclass/protocols/arrow_loop.py
from __future__ import annotations

from typing import Protocol, TypeVar, Generic, runtime_checkable

from typeclass.protocols.arrow import Arrow

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@runtime_checkable
class ArrowLoop(Arrow[A, B], Protocol, Generic[A, B]):
    """
    ArrowLoop typeclass.

    ArrowLoop extends Arrow with *feedback*: you can feed part of an arrow’s
    output back into its input, creating cyclic dataflow.

    Core operation:
        loop : arr (a, c) (b, c) -> arr a b

    Intuition:
      - You build an arrow that, given (a, c_in), produces (b, c_out).
      - `loop` ties the knot by setting c_in = c_out, leaving a as the only
        external input and b as the external output.

    Informal semantics:
        loop(f)(a) = b
        where (b, c) = f(a, c)

    This is a *fixed point* / knot-tying principle, and real implementations
    generally require some notion of laziness, guardedness, or domain-theoretic
    structure to be total. In practice, you’ll decide what “loop” means for
    your interpreter/backend (lazy tuples, explicit delay nodes, etc.).

    Laws (informal; common ArrowLoop laws):

    - Naturality with `arr` (for functions that only rearrange structure):
        loop(arr(assoc) >>> f >>> arr(unassoc)) == loop(f)
      where assoc/unassoc are tuple reassociations appropriate for your
      canonical nesting.

    - Vanishing (feedback over trivial wire):
        loop(arr(lambda (a, c): (g(a), c))) == arr(g)
      (expressed more carefully in languages with pattern matching)

    Notes for your AST/syntax setup:
      - This is the node that turns a DAG into a cyclic graph.
      - If you later add GraphIR + scheduling, loop is where you need explicit
        handling: you may represent it as a strongly-connected component (SCC)
        with chosen evaluation strategy (iterate to fixpoint, lazy tie, etc.).
      - It’s okay if your first interpreter supports only “productive” loops
        (where the feedback is lazily demanded) or rejects/guards others.
    """

    @classmethod
    def loop(cls, self: ArrowLoop[tuple[A, C], tuple[B, C]]) -> ArrowLoop[A, B]:
        """
        Tie a feedback loop on the second component.

        Given:
            self : arr (a, c) (b, c)

        Produce:
            loop(self) : arr a b

        Informally:
            loop(f)(a) = b
            where (b, c) = f(a, c)

        Returns:
            ArrowLoop[A, B]
        """
        ...
