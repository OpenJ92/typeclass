from typeclass.data.maybe import Just, Nothing, Maybe
from typeclass.data.tree import Tree
from typeclass.data.sequence import Sequence
from typeclass.data.streamtree import StreamTree
from typeclass.data.stream import Stream
from typeclass.data.thunk import suspend

from typeclass.interpret.run import evaluate

from typeclass.typeclasses.symbols import pure, ap

def realize(tree: StreamTree[Maybe[A]]) -> Tree[A]:
    match tree.value:
        case Just(value=v):
            return Tree(v, _realize_children(tree.children.force()))
        case Nothing():
            raise ValueError("cannot project a root Nothing() into Tree")


def _realize_children(
    children,
) -> Sequence[Tree[A]]:
    out = []

    cur = children
    while True:
        child = cur.head

        match child.value:
            case Just():
                out.append(realize(child))
                cur = cur.tail.force()
            case Nothing():
                return Sequence(tuple(out))


def depths(depth: int = 0) -> StreamTree[int]:
    return StreamTree(depth, suspend(Stream.pure, suspend(depths, depth+1)))


def widths(width: int = 0) -> StreamTree[int]:
    return StreamTree(width, suspend(_width_children))

def _width_children() -> Stream[StreamTree[int]]:
    def build(i: int) -> Stream[StreamTree[int]]:
        return suspend(Stream, widths(i), suspend(build, i + 1))
    return build(0)

def coordinates() -> StreamTree[tuple[int, int]]:
    return evaluate(StreamTree |pure| (lambda x: lambda y: (x, y)) |ap| depths() |ap| widths())

def paths(path: tuple[int, ...] = ()) -> StreamTree[tuple[int, ...]]:
    return StreamTree(path, suspend(_path_children, path))


def _path_children(path: tuple[int, ...]) -> Stream[StreamTree[tuple[int, ...]]]:
    def build(i: int) -> Stream[StreamTree[tuple[int, ...]]]:
        return Stream(paths(path + (i,)), suspend(build, i + 1),)

    return build(0)
