from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.monad import Monad
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq
from typeclass.protocols.force import Force

S = TypeVar("S")   # threaded state
A = TypeVar("A")   # contained value
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True)
class State(
    Monad[A],
    Applicative[A],
    Functor[A],
    Show,
    Eq,
    Generic[S, A],
):
    _run: Callable[[S], tuple[A, S]]

    # --- core --------------------------------------------------------------

    def run(self, state: S) -> tuple[A, S]:
        return self._run(state)

    def eval(self, state: S) -> A:
        value, _ = self.run(state)
        return value

    def exec(self, state: S) -> S:
        _, next_state = self.run(state)
        return next_state

    # --- Functor -----------------------------------------------------------

    def fmap(self: State[S, A], f: Force[Callable[[A], B]]) -> State[S, B]:
        def inner(state: S) -> tuple[B, S]:
            value, next_state = self.run(state)
            return (f.force()(value), next_state)

        return State(inner)

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> State[S, A]:
        def inner(state: S) -> tuple[A, S]:
            return (value, state)

        return State(inner)

    def ap(self: State[S, Callable[[A], B]], fa: Force[State[S, A]]) -> State[S, B]:
        def inner(state: S) -> tuple[B, S]:
            function, state1 = self.run(state)
            value, state2 = fa.force().run(state1)
            return (function(value), state2)

        return State(inner)

    # --- Monad -------------------------------------------------------------

    def bind(self: State[S, A], fm: Force[Callable[[A], State[S, B]]]) -> State[S, B]:
        def inner(state: S) -> tuple[B, S]:
            value, state1 = self.run(state)
            next_state = fm.force()(value)
            return next_state.run(state1)

        return State(inner)

    # --- Show / Eq ---------------------------------------------------------

    def show(self) -> str:
        return f"State({self._run!r})"

    def eq(self, other: object) -> bool:
        # Extensional equality is undecidable in general.
        # Keep this structural, same as Reader.
        return isinstance(other, State) and self._run is other._run


