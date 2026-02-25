from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Any, cast

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.monad import Monad
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq

A = TypeVar("A")   # environment / input
B = TypeVar("B")   # output / contained
C = TypeVar("C")
D = TypeVar("D")


@dataclass(frozen=True)
class Function(Monad, Applicative[B], Functor[B], Show, Eq, Generic[A, B]):
    """
    Reader / (->) A  as a type constructor in B.

    Think: Function[A, B] ~ (A -> B)

    Instances (pointwise, at the same A):
      Functor:      fmap f (g)   = f ∘ g
      Applicative:  pure b       = const b
                    ap fg gx     = \a -> fg(a)(gx(a))
      Monad:        bind g k     = \a -> k(g(a))(a)
    """

    _run: Callable[[A], B]

    # --- core --------------------------------------------------------------

    def run(self, a: A) -> B:
        return self._run(a)

    def __call__(self, a: A) -> B:
        return self._run(a)

    # --- Functor -----------------------------------------------------------

    def fmap(self: Function[A, B], f: Callable[[B], C]) -> Function[A, C]:
        def inner(a: A) -> C:
            return f.force()(self.run(a))
        return Function(inner)

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls: type, value: B) -> Function[A, B]:
        def inner(_: A) -> B:
            return value
        return Function(inner)

    def ap(self: Function[A, Callable[[B], C]], fb: Function[A, B]) -> Function[A, C]:
        def inner(a: A) -> C:
            return func(fb.force().run(a))
        return Function(inner)

    # --- Monad -------------------------------------------------------------

    def bind(self: Function[A, B], fm: Callable[[B], Function[A, C]]) -> Function[A, C]:
        def inner(a: A) -> C:
            return fm_(self.run(a)).run(a)
        return Function(inner)

    # --- Show / Eq ---------------------------------------------------------

    def show(self) -> str:
        return f"Function({self._run!r})"

    def eq(self, other: object) -> bool:
        # Extensional equality is undecidable in general; keep it structural.
        return isinstance(other, Function) and self._run is other._run
