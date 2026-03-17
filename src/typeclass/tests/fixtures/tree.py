from typeclass.data.sequence import Sequence
from typeclass.data.tree import Tree


def leaf():
    return Tree(1, Sequence(()))


def shallow():
    return Tree(
        1,
        Sequence((
            Tree(2, Sequence(())),
            Tree(3, Sequence(())),
        )),
    )


def deep():
    return Tree(
        10,
        Sequence((
            Tree(
                20,
                Sequence((
                    Tree(30, Sequence(())),
                )),
            ),
        )),
    )


def values():
    return [leaf(), shallow(), deep()]


def replacement():
    return "x"


def pure_values():
    return [0, 1, 10]


def function_values():
    return [
        Tree(lambda x: x + 1, Sequence(())),
        Tree(
            lambda x: x * 2,
            Sequence((
                Tree(lambda x: x - 1, Sequence(())),
            )),
        ),
    ]


def composition_function_values():
    return (
        [
            Tree(lambda x: x + 1, Sequence(())),
            Tree(
                lambda x: x * 2,
                Sequence((
                    Tree(lambda x: x - 1, Sequence(())),
                )),
            ),
        ],
        [
            Tree(lambda x: x - 3, Sequence(())),
            Tree(
                lambda x: x * x,
                Sequence((
                    Tree(lambda x: x + 4, Sequence(())),
                )),
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
        lambda x: Tree(x, Sequence(())),
        lambda x: Tree(
            x + 1,
            Sequence((
                Tree(x * 2, Sequence(())),
            )),
        ),
        lambda x: Tree(
            x - 1,
            Sequence((
                Tree(x + 10, Sequence(())),
                Tree(x + 20, Sequence(())),
            )),
        ),
    ]


def join_values():
    return [
        Tree(Tree(1, Sequence(())), Sequence(())),
        Tree(
            Tree(
                1,
                Sequence((
                    Tree(2, Sequence(())),
                )),
            ),
            Sequence((
                Tree(Tree(3, Sequence(())), Sequence(())),
            )),
        ),
        Tree(
            Tree(
                10,
                Sequence((
                    Tree(20, Sequence(())),
                )),
            ),
            Sequence((
                Tree(
                    Tree(30, Sequence(())),
                    Sequence(()),
                ),
            )),
        ),
    ]
