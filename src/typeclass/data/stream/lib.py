from typing import Callable, TypeVar

from typeclass.data.thunk import Thunk
from typeclass.data.stream.core import Stream
from typeclass.data.sequence import Sequence, Cons, Nil

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def repeat(value: A) -> Stream[A]:
    return Stream(value, Thunk(lambda: repeat(value)))


def iterate(function: Callable[[A], A], seed: A) -> Stream[A]:
    return Stream(seed, Thunk(lambda: iterate(function, function(seed))))


def unfold(step: Callable[[A], tuple[B, A]], seed: A) -> Stream[B]:
    value, next_seed = step(seed)
    return Stream(value, Thunk(lambda: unfold(step, next_seed)))


def head(stream: Stream[A]) -> A:
    return stream.head


def tail(stream: Stream[A]) -> Stream[A]:
    return stream.tail.force()


def nth(stream: Stream[A], index: int) -> A:
    if index < 0:
        raise ValueError("nth expects a non-negative index")

    cur = stream
    for _ in range(index):
        cur = cur.tail.force()
    return cur.head


def drop(count: int, stream: Stream[A]) -> Stream[A]:
    if count < 0:
        raise ValueError("drop expects a non-negative count")

    cur = stream
    for _ in range(count):
        cur = cur.tail.force()
    return cur


def take(count: int, stream: Stream[A]) -> Sequence[A]:
    if count < 0:
        raise ValueError("take expects a non-negative count")

    if count == 0:
        return Nil()

    return Cons(stream.head, take(count - 1, stream.tail.force()))


def map_stream(function: Callable[[A], B], stream: Stream[A]) -> Stream[B]:
    return stream.fmap(Thunk(lambda: function))


def prepend(value: A, stream: Stream[A]) -> Stream[A]:
    return Stream(value, Thunk(lambda: stream))


def zip_with(function: Callable[[A, B], C], xs: Stream[A], ys: Stream[B]) -> Stream[C]:
    return Stream(
        function(xs.head, ys.head),
        Thunk(lambda: zip_with(function, xs.tail.force(), ys.tail.force())),
    )


def zip_stream(xs: Stream[A], ys: Stream[B]) -> Stream[tuple[A, B]]:
    return zip_with(lambda x, y: (x, y), xs, ys)


def interleave(xs: Stream[A], ys: Stream[A]) -> Stream[A]:
    return Stream(
        xs.head,
        Thunk(lambda: Stream(ys.head, Thunk(lambda: interleave(xs.tail.force(), ys.tail.force())))),
    )


def scanl(function: Callable[[B, A], B], initial: B, stream: Stream[A]) -> Stream[B]:
    next_value = function(initial, stream.head)
    return Stream(
        initial,
        Thunk(lambda: scanl(function, next_value, stream.tail.force())),
    )


def tails(stream: Stream[A]) -> Stream[Stream[A]]:
    return Stream(
        stream,
        Thunk(lambda: tails(stream.tail.force())),
    )


# --------------------------------------------------------------------------
# Sequence conversions
# --------------------------------------------------------------------------

def cycle_sequence(xs: Sequence[A]) -> Stream[A]:
    """
    Turn a non-empty finite Sequence into a Stream by cycling forever.
    """
    match xs:
        case Nil():
            raise ValueError("cannot cycle an empty Sequence into a Stream")
        case _:
            return _cycle_from_root(xs, xs)


def _cycle_from_root(root: Sequence[A], current: Sequence[A]) -> Stream[A]:
    match current:
        case Cons(head=h, tail=t):
            return Stream(h, Thunk(lambda: _cycle_from_root(root, t)))
        case Nil():
            return _cycle_from_root(root, root)


def repeat_last(xs: Sequence[A]) -> Stream[A]:
    """
    Turn a non-empty finite Sequence into a Stream by repeating the final value.
    """
    match xs:
        case Nil():
            raise ValueError("cannot extend an empty Sequence into a Stream")
        case Cons(head=h, tail=Nil()):
            return Stream(h, Thunk(lambda: repeat(h)))
        case Cons(head=h, tail=t):
            return Stream(h, Thunk(lambda: repeat_last(t)))


def prefix(stream: Stream[A], count: int) -> Sequence[A]:
    return take(count, stream)
