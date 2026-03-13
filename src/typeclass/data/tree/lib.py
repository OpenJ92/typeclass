from typeclass.data.sequence import Nil

from typing import TypeVar

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
    if tree.children == Nil():
        return 1
    return 1 + max(depth(child) for child in tree.children)
