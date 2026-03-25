from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Any, cast

from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.semigroup import Semigroup
from typeclass.typeclasses.monoid import Monoid
from typeclass.typeclasses.semigroupoid import Semigroupoid
from typeclass.typeclasses.category import Category
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.eq import Eq

A = TypeVar("A")   # environment / input
B = TypeVar("B")   # output / contained
C = TypeVar("C")

@dataclass(frozen=True)
class Reader(Monad[B], Applicative[B], Functor[B], Show, Eq, Generic[A, B]):
    """
    Reader / (->) A  as a type constructor in B.

    Think: Reader[A, B] ~ (A -> B)

    Instances (pointwise, at the same A):
      Functor:      fmap f (g)   = f ∘ g
      Applicative:  pure b       = const b
                    ap fg gx     = \a -> fg(a)(gx(a))
      Monad:        bind g k     = \a -> k(g(a))(a)
    """

    _run : Callable[[A], B]

    # --- core --------------------------------------------------------------

    def run(self, a: A) -> B:
        return self._run(a)

    # --- Functor -----------------------------------------------------------

    def fmap(self: Reader[A, B], f: Callable[[B], C]) -> Reader[A, C]:
        def inner(a: A) -> C:
            function = f.force()
            value = self.run(a)
            return function(value)
        return Reader(inner)

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls: type, value: B) -> Reader[A, B]:
        def inner(_: A) -> B:
            return value
        return Reader(inner)

    def ap(self: Reader[A, Callable[[B], C]], fb: Reader[A, B]) -> Reader[A, C]:
        def inner(a: A) -> C:
            function = self.run(a)
            value = fb.force().run(a)
            return function(value)
        return Reader(inner)

    # --- Monad -------------------------------------------------------------

    def bind(self: Reader[A, B], fm: Callable[[B], Reader[A, C]]) -> Reader[A, C]:
        def inner(a: A) -> C:
            value = self.run(a)
            function = fm.force()(value)
            return function.run(a)
        return Reader(inner)
    
    # --- Show / Eq ---------------------------------------------------------

    def show(self) -> str:
        return f"Reader({self._run!r})"

    def eq(self, other: object) -> bool:
        # Extensional equality is undecidable in general; keep it structural.
        return isinstance(other, Reader) and self._run is other._run
