from typeclass.data.maybe import Just, Nothing, Maybe
from typeclass.data.tree import Tree
from typeclass.data.sequence import Sequence


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
