from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.monad import Monad
from typeclass.protocols.monoid import Monoid
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq

W = TypeVar("W", bound=Monoid)  # log
A = TypeVar("A")                # value / contained
B = TypeVar("B")


@dataclass(frozen=True)
class Writer(Monad[A], Applicative[A], Functor[A], Show, Eq, Generic[W, A]):
    """
    Writer[W, A] = (A, W)

    W must be a Monoid.

    Instances:
      Functor:      fmap f (a, w)   = (f a, w)
      Applicative:  pure a          = (a, mempty)
                    ap (f, w1) (a, w2) = (f a, w1 <> w2)
      Monad:        bind (a, w1) k  = let (b, w2) = k a in (b, w1 <> w2)
    """

    value: A
    log: W

    # --- core --------------------------------------------------------------

    def run(self) -> tuple[A, W]:
        return (self.value, self.log)

    # --- Functor -----------------------------------------------------------

    def fmap(self: Writer[W, A], f: Callable[[A], B]) -> Writer[W, B]:
        def inner() -> Writer[W, B]:
            function = f.force()
            return Writer(function(self.value), self.log)
        return inner()

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls: type, _: A) -> Writer[W, A]:
        raise TypeError(
            "Writer.pure needs the log type. Use Writer.pure_with(W, value)."
        )

    @classmethod
    def pure_with(cls, Wcls: type[W], value: A) -> Writer[W, A]:
        return Writer(value, Wcls.mempty())  # type: ignore[attr-defined]

    def ap(self: Writer[W, Callable[[A], B]], fa: Writer[W, A]) -> Writer[W, B]:
        def inner() -> Writer[W, B]:
            function = self.value
            return Writer(function(fa.value), self.log.combine(fa.log))
        return inner()

    # --- Monad -------------------------------------------------------------

    def bind(self: Writer[W, A], fm: Callable[[A], Writer[W, B]]) -> Writer[W, B]:
        def inner() -> Writer[W, B]:
            function = fm.force()
            wb = function(self.value)
            return Writer(wb.value, self.log.combine(wb.log))
        return inner()

    # --- Show / Eq ---------------------------------------------------------

    def show(self) -> str:
        return f"Writer(value={self.value!r}, log={self.log!r})"

    def eq(self, other: object) -> bool:
        return (
            isinstance(other, Writer)
            and self.value == other.value
            and self.log == other.log
        )
