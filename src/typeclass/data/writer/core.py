from dataclasses import dataclass
from functools import cache
from typing import Callable, Generic, TypeVar

from typeclass.data.thunk import Thunk

from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.eq import Eq
from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.monoid import Monoid
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.force import Force

W = TypeVar("W", bound=Monoid)
A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class WriterBase(
    Monad[A],
    Applicative[A],
    Functor[A],
    Show,
    Eq,
    Generic[W, A],
):
    """
    Generic Writer container.

        WriterBase[W, A] = (A, W)

    This is the implementation substrate only. Public usage should go
    through `Writer(Wcls)`, which fixes the log monoid and returns a
    specialized unary constructor with a lawful `pure`.
    """

    value: A
    log: W

    def run(self) -> tuple[A, W]:
        return (self.value, self.log)

    def fmap(self: WriterBase[W, A], f: Force[Callable[[A], B]]) -> WriterBase[W, B]:
        return type(self)(f.force()(self.value), self.log)

    @classmethod
    def pure(cls: type, _: A) -> WriterBase[W, A]:
        raise TypeError(
            f"{cls.__name__}.pure(value) requires a fixed log monoid. "
            "Use Writer(LogType).pure(value)."
        )

    def ap(
        self: WriterBase[W, Callable[[A], B]],
        fa: Force[WriterBase[W, A]],
    ) -> WriterBase[W, B]:
        wa = fa.force()
        return type(self)(
            self.value(wa.value),
            self.log.combine(Thunk(lambda: wa.log)),
        )

    def bind(
        self: WriterBase[W, A],
        fm: Force[Callable[[A], WriterBase[W, B]]],
    ) -> WriterBase[W, B]:
        wb = fm.force()(self.value)
        return type(self)(
            wb.value,
            self.log.combine(Thunk(lambda: wb.log)),
        )

    def show(self) -> str:
        return f"{type(self).__name__}(value={self.value!r}, log={self.log!r})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, WriterBase)
            and self.value == other.value
            and self.log == other.log
        )


@cache
def Writer(Wcls: type[W]):
    """
    Specialize WriterBase at a fixed log monoid type.

    Example
    -------
        WriterSequence = Writer(Sequence)
        x = WriterSequence.pure(10)
    """

    @dataclass(frozen=True)
    class _Writer(WriterBase[W, A]):
        @classmethod
        def pure(cls: type, value: A) -> _Writer:
            return cls(value, Wcls.mempty())

    _Writer.__name__ = f"Writer({Wcls.__name__})"
    return _Writer
