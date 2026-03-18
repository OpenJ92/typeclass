from typeclass.data.sequence.core import Sequence

from typing import TypeVar, Callable

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def from_iterable(iterable):
    """
    Construct a Sequence from any iterable.
    
    Elements are inserted in the same order as the iterable.
    """
    return Sequence(iterable)


def length(xs: Sequence[A]) -> int:
    return length(xs)


def zipwith(function: Callable[[A, B], C], xs: Sequence[A], ys: Sequence[B]) -> Sequence[C]:
    return (function(x, y) for x, y in zip(xs, ys))
            
def concat(xs: Sequence[A], ys: Sequence[A]) -> Sequence[A]:
    return Sequence(xs._values + ys._values)
