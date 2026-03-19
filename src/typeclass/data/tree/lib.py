from typing import TypeVar
from typeclass.data.maybe import Just, Nothing, Maybe
from typeclass.data.tree import Tree
from typeclass.data.stream import Stream
from typeclass.data.streamtree import StreamTree
from typeclass.data.thunk import Thunk
from typeclass.data.sequence import Sequence

A = TypeVar("A")

def pretty(tree: Tree[A], prefix: str="", is_last: bool=True) -> str:
    connector = "└─ " if is_last else "├─ "
    print(prefix + connector + repr(tree.value))

    children = list(tree.children)
    next_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(children):
        pretty(child, next_prefix, i == len(children) - 1)


def size(tree: Tree[A]) -> int:
    return 1 + sum(size(child) for child in tree.children)


def depth(tree: Tree[A]) -> int:
    if not tree.children:
        return 1
    return 1 + max(depth(child) for child in tree.children)


def embed(tree: Tree[A]) -> StreamTree[Maybe[A]]:
    return StreamTree(
        Just(tree.value),
        Thunk(lambda: _sequence_children_to_stream(tree.children)),
    )


def _sequence_children_to_stream(
    children: Sequence[Tree[A]],
) -> Stream[StreamTree[Maybe[A]]]:
    xs = tuple(children)

    if not xs:
        return Stream.pure(_empty_streamtree())

    return _stream_from_tuple(xs, 0)


def _stream_from_tuple(
    xs: tuple[Tree[A], ...],
    index: int,
) -> Stream[StreamTree[Maybe[A]]]:
    if index < len(xs):
        head = embed(xs[index])
        return Stream(
            head,
            Thunk(lambda: _stream_from_tuple(xs, index + 1)),
        )

    return Stream.pure(_empty_streamtree())


def _empty_streamtree() -> StreamTree[Maybe[A]]:
    return StreamTree(
        Nothing(),
        Thunk(lambda: Stream.pure(_empty_streamtree())),
    )
