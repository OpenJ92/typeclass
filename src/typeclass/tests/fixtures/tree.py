from typeclass.data.sequence import Nil, Cons
from typeclass.data.tree import Tree


def leaf():
    return Tree(1, Nil())


def shallow():
    return Tree(
        1,
        Cons(Tree(2, Nil()), Cons(Tree(3, Nil()), Nil())),
    )


def deep():
    return Tree(
        10,
        Cons(
            Tree(20, Cons(Tree(30, Nil()), Nil())),
            Nil(),
        ),
    )


def values():
    return [leaf(), shallow(), deep()]


def replacement():
    return "x"


def pure_values():
    return [0, 1, 10]


def function_values():
    return [
        Tree(lambda x: x + 1, Nil()),
        Tree(
            lambda x: x * 2,
            Cons(Tree(lambda x: x - 1, Nil()), Nil()),
        ),
    ]


def composition_function_values():
    return (
        [
            Tree(lambda x: x + 1, Nil()),
            Tree(
                lambda x: x * 2,
                Cons(Tree(lambda x: x - 1, Nil()), Nil()),
            ),
        ],
        [
            Tree(lambda x: x - 3, Nil()),
            Tree(
                lambda x: x * x,
                Cons(Tree(lambda x: x + 4, Nil()), Nil()),
            ),
        ],
    )


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: Tree(x, Nil()),
        lambda x: Tree(x + 1, Cons(Tree(x * 2, Nil()), Nil())),
        lambda x: Tree(
            x - 1,
            Cons(Tree(x + 10, Nil()), Cons(Tree(x + 20, Nil()), Nil())),
        ),
    ]


def join_values():
    return [
        Tree(Tree(1, Nil()), Nil()),
        Tree(
            Tree(1, Cons(Tree(2, Nil()), Nil())),
            Cons(
                Tree(Tree(3, Nil()), Nil()),
                Nil(),
            ),
        ),
        Tree(
            Tree(
                10,
                Cons(Tree(20, Nil()), Nil()),
            ),
            Cons(
                Tree(
                    Tree(30, Nil()),
                    Nil(),
                ),
                Nil(),
            ),
        ),
    ]
