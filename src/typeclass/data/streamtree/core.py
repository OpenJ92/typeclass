from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.data.stream import Stream
from typeclass.data.stream.lib import _zipwith
from typeclass.data.thunk import Thunk, delay, suspend, resume
from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.comonad import Comonad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.force import Force

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True, eq=False, repr=False)
class StreamTree(
    Comonad[A],
    Applicative[A],
    Functor[A],
    Show,
    Generic[A],
):
    value: A
    children: Force[Stream[StreamTree[A]]]

    EQ_DEPTH = 2
    EQ_BREADTH = 2

    # ----- Functor ---------------------------------------------------------

    def fmap(self, f: Force[Callable[[A], B]]) -> StreamTree[B]:
        nf = f.force()
        children = self.children.force()

        return StreamTree(
            nf(self.value),
            Thunk(lambda: children.fmap(delay(lambda child: child.fmap(f))))
        )
        

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls, value: A) -> StreamTree[A]:
        return StreamTree(
            value,
            Thunk(lambda: Stream.pure(cls.pure(value))),
        )

    def ap(self: StreamTree[Callable[[A], B]], fa: Force[StreamTree[A]]) -> StreamTree[B]:
        other = fa.force()
        return StreamTree(
            self.value(other.value),
            suspend(_zipwith, lambda x, y: x.ap(delay(y)), self.children, other.children)
        )

    # ----- Comonad ---------------------------------------------------------

    def extract(self) -> A:
        return self.value

    def duplicate(self) -> StreamTree[StreamTree[A]]:
        children = self.children.force()

        return StreamTree(
            self,
            Thunk(lambda: children.fmap(delay(lambda child: child.duplicate()))),
        )

    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        return f"StreamTree(value={self.value!r}, children=<{self.children}>)"

    # ----- Eq --------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StreamTree):
            return False
        return _eq_streamtree(self, other, self.EQ_DEPTH, self.EQ_BREADTH)

    # ----- Convenience -----------------------------------------------------

def _eq_streamtree(
    left:  StreamTree[A],
    right: StreamTree[A],
    depth: int,
    breadth: int,
) -> bool:

    if left.value != right.value:
        return False

    if depth <= 0:
        return True

    lx = left.children.force()
    rx = right.children.force()

    for _ in range(breadth):
        if not _eq_streamtree(lx.head, rx.head, depth - 1, breadth):
            return False
        lx = lx.tail.force()
        rx = rx.tail.force()

    return True
