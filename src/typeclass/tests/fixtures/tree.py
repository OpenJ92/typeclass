from typeclass.data.sequence import Nil, Cons
from typeclass.data.tree import Tree


def leaf():
    return Tree(1, Nil())


def shallow():
    return Tree(
        1,
        Cons(
            Tree(2, Nil()),
            Cons(
                Tree(3, Nil()),
                Nil(),
            ),
        ),
    )


def deep():
    return Tree(
        10,
        Cons(
            Tree(
                20,
                Cons(
                    Tree(30, Nil()),
                    Nil(),
                ),
            ),
            Nil(),
        ),
    )


def values():
    return [
        leaf(),
        shallow(),
        deep(),
    ]


def replacement():
    return "x"
