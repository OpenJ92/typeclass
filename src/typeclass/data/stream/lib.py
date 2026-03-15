from typing import Callable, TypeVar

from typeclass.data.thunk import Thunk
from typeclass.data.stream.core import Stream
from typeclass.data.sequence import Sequence, Cons, Nil

from typeclass.syntax.symbols import pure, ap, duplicate

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def _repeat(value: A) -> Stream[A]:
    """
    Construct an infinite Stream where every element is the same value.

    Args:
        value: The value to repeat forever.

    Returns:
        A Stream whose head and every subsequent element are `value`.
    """
    return Stream(value, Thunk(lambda: _repeat(value)))


def _iterate(function: Callable[[A], A], seed: A) -> Stream[A]:
    """
    Construct an infinite Stream by repeatedly applying a function to a seed.

    The first element is the seed itself. Each following element is produced
    by applying `function` to the previous one.

    Args:
        function: A function from A to A used to generate successive values.
        seed: The initial value of the Stream.

    Returns:
        A Stream beginning at `seed` and continuing with repeated applications
        of `function`.
    """
    return Stream(seed, Thunk(lambda: _iterate(function, function(seed))))


def _unfold(step: Callable[[A], tuple[B, A]], seed: A) -> Stream[B]:
    """
    Construct an infinite Stream from a seed value and a stepping function.

    The step function produces the next output value along with the next seed.

    Args:
        step: A function that takes a seed of type A and returns a pair
            containing the next value of type B and the next seed of type A.
        seed: The initial seed value.

    Returns:
        A Stream of values produced by repeatedly applying `step`.
    """
    value, next_seed = step(seed)
    return Stream(value, Thunk(lambda: _unfold(step, next_seed)))


def _head(stream: Stream[A]) -> A:
    """
    Extract the first element of a Stream.

    Args:
        stream: The Stream from which to take the first element.

    Returns:
        The head value of the Stream.
    """
    return stream.head


def _tail(stream: Stream[A]) -> Stream[A]:
    """
    Extract the tail of a Stream.

    Args:
        stream: The Stream from which to take the tail.

    Returns:
        A Stream containing every element after the head.
    """
    return stream.tail.force()


def _nth(stream: Stream[A], index: int) -> A:
    """
    Extract the element at a given zero-based index from a Stream.

    Args:
        stream: The Stream to index into.
        index: The zero-based position of the desired element.

    Returns:
        The value at the given index in the Stream.

    Raises:
        ValueError: If `index` is negative.
    """
    if index < 0:
        raise ValueError("nth expects a non-negative index")

    cur = stream
    for _ in range(index):
        cur = cur.tail.force()
    return cur.head


def _drop(count: int, stream: Stream[A]) -> Stream[A]:
    """
    Skip a number of elements from the front of a Stream.

    Args:
        count: The number of elements to discard.
        stream: The Stream to drop elements from.

    Returns:
        The Stream remaining after the first `count` elements are removed.

    Raises:
        ValueError: If `count` is negative.
    """
    if count < 0:
        raise ValueError("drop expects a non-negative count")

    cur = stream
    for _ in range(count):
        cur = cur.tail.force()
    return cur


def _take(count: int, stream: Stream[A]) -> Sequence[A]:
    """
    Take a finite prefix of a Stream as a Sequence.

    Args:
        count: The number of elements to take.
        stream: The Stream from which to take elements.

    Returns:
        A finite Sequence containing the first `count` elements of the Stream.

    Raises:
        ValueError: If `count` is negative.
    """
    if count < 0:
        raise ValueError("take expects a non-negative count")

    if count == 0:
        return Nil()

    return Cons(stream.head, _take(count - 1, stream.tail.force()))


def _prepend(value: A, stream: Stream[A]) -> Stream[A]:
    """
    Add a value to the front of a Stream.

    Args:
        value: The value to place at the head of the new Stream.
        stream: The Stream that will follow the prepended value.

    Returns:
        A Stream whose head is `value` and whose tail is `stream`.
    """
    return Stream(value, Thunk(lambda: stream))


def _zipwith(function: Callable[[A, B], C], xs: Stream[A], ys: Stream[B]) -> Stream[C]:
    """
    Combine two Streams elementwise using a binary function.

    Args:
        function: A function that combines one element from `xs`
            and one element from `ys`.
        xs: The first Stream.
        ys: The second Stream.

    Returns:
        A Stream whose elements are produced by applying `function`
        to corresponding elements of `xs` and `ys`.
    """
    return Stream |pure| function |ap| xs |ap| ys


def _zip_stream(xs: Stream[A], ys: Stream[B]) -> Stream[tuple[A, B]]:
    """
    Pair corresponding elements from two Streams.

    Args:
        xs: The first Stream.
        ys: The second Stream.

    Returns:
        A Stream of pairs where each element contains one value from `xs`
        and the corresponding value from `ys`.
    """
    return Stream |pure| curry(lambda x, y: (x, y)) |ap| xs |ap| ys


def _interleave(xs: Stream[A], ys: Stream[A]) -> Stream[A]:
    """
    Alternate elements from two Streams.

    Args:
        xs: The first Stream.
        ys: The second Stream.

    Returns:
        A Stream whose elements alternate between `xs` and `ys`.
    """
    return Stream(
        xs.head,
        Thunk(lambda: Stream(ys.head, Thunk(lambda: _interleave(xs.tail.force(), ys.tail.force())))),
    )


def _scanl(function: Callable[[B, A], B], initial: B, stream: Stream[A]) -> Stream[B]:
    """
    Produce the Stream of successive left-fold accumulations.

    The first element is the initial accumulator. Each following element is
    produced by combining the current accumulator with the next stream value.

    Args:
        function: A function that combines the accumulator with a stream value.
        initial: The initial accumulator value.
        stream: The input Stream.

    Returns:
        A Stream of accumulated values.
    """
    next_value = function(initial, stream.head)
    return Stream(
        initial,
        Thunk(lambda: _scanl(function, next_value, stream.tail.force())),
    )


def _tails(stream: Stream[A]) -> Stream[Stream[A]]:
    """
    Produce the Stream of all suffixes of a Stream.

    The first element is the original Stream, the next is its tail, and so on.

    Args:
        stream: The Stream whose suffixes should be produced.

    Returns:
        A Stream of Streams, where each element is a tail of the original Stream.
    """
    return duplicate(stream)


def _cycle_sequence(xs: Sequence[A]) -> Stream[A]:
    """
    Turn a non-empty finite Sequence into a Stream by cycling forever.

    Args:
        xs: A finite, non-empty Sequence.

    Returns:
        A Stream that repeats the elements of `xs` indefinitely.

    Raises:
        ValueError: If `xs` is empty.
    """
    match xs:
        case Nil():
            raise ValueError("cannot cycle an empty Sequence into a Stream")
        case _:
            return __cycle_from_root(xs, xs)


def __cycle_from_root(root: Sequence[A], current: Sequence[A]) -> Stream[A]:
    """
    Continue cycling through a root Sequence from a current position.

    Args:
        root: The original Sequence to cycle through repeatedly.
        current: The current remaining suffix of `root`.

    Returns:
        A Stream that traverses `current`, restarting from `root`
        whenever the end is reached.
    """
    match current:
        case Cons(head=h, tail=t):
            return Stream(h, Thunk(lambda: __cycle_from_root(root, t)))
        case Nil():
            return __cycle_from_root(root, root)


def _repeat_last(xs: Sequence[A]) -> Stream[A]:
    """
    Turn a non-empty finite Sequence into a Stream by repeating the final value.

    Args:
        xs: A finite, non-empty Sequence.

    Returns:
        A Stream that follows the elements of `xs` once and then repeats
        the final element forever.

    Raises:
        ValueError: If `xs` is empty.
    """
    match xs:
        case Nil():
            raise ValueError("cannot extend an empty Sequence into a Stream")
        case Cons(head=h, tail=Nil()):
            return Stream(h, Thunk(lambda: repeat(h)))
        case Cons(head=h, tail=t):
            return Stream(h, Thunk(lambda: _repeat_last(t)))


def _prefix(stream: Stream[A], count: int) -> Sequence[A]:
    """
    Extract a finite prefix of a Stream as a Sequence.

    Args:
        stream: The Stream from which to take a prefix.
        count: The number of elements to include.

    Returns:
        A Sequence containing the first `count` elements of the Stream.
    """
    return take(count, stream)
