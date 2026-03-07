# src/typeclass/protocols/arrow_apply.py
from __future__ import annotations

from typing import Protocol, TypeVar, Generic, runtime_checkable

from typeclass.protocols.arrow import Arrow

A = TypeVar("A")
B = TypeVar("B")


@runtime_checkable
class ArrowApply(Arrow[A, B], Protocol, Generic[A, B]):
    """
    ArrowApply typeclass.

    ArrowApply extends Arrow with an “application” operator that lets you
    *apply an arrow-valued value* to an input value *within the arrow world*.

    Intuition:
      - Arrow is “static wiring”: you build a graph, but the shape is fixed.
      - ArrowApply introduces a controlled form of “dynamic wiring” by allowing
        a value to *contain an arrow* and then applying it.

    Core operation:
        app : arr (arr a b, a) b

    Semantics of `app`:
        app((f, a)) = f(a)

    but crucially this happens *inside* the Arrow instance, so `f` is an Arrow,
    not a raw Python function.

    Laws (informal; typical ArrowApply laws):

    - Application respects arr:
        app ∘ arr(lambda a: (arr(f), a)) == arr(f)

      i.e. if you pack a lifted pure function arrow with its input, `app`
      behaves like ordinary application.

    - Coherence with composition (implementation-dependent but standard):
      `app` should behave like the evaluator for the arrow language.

    Notes for your project:
      - In an AST, `app` is the node that “runs” an arrow held in data.
      - Many graph optimizations become harder once ArrowApply is present,
        because the structure can become input-dependent.
      - Still very useful for DSLs, interpreters, staged computation, etc.
    """

    @classmethod
    def app(cls) -> ArrowApply[tuple[ArrowApply[A, B], A], B]:
        """
        Apply an arrow to an input inside the arrow.

            app((f, a)) == f(a)

        Returns:
            ArrowApply[tuple[ArrowApply[A, B], A], B]
        """
        ...
