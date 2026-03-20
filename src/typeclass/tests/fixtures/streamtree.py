from typeclass.data.streamtree import StreamTree
from typeclass.data.streamtree.lib import depths, widths, paths


def values():
    return [
        StreamTree.pure(0),
        StreamTree.pure(3),
        depths(),
        widths(),
    ]


def replacement():
    return "x"


def pure_values():
    return [0, 1, 10]


def function_values():
    return [
        StreamTree.pure(lambda x: x + 1),
        StreamTree.pure(lambda x: x * 2),
    ]


def composition_function_values():
    return (
        [
            StreamTree.pure(lambda x: x + 1),
            StreamTree.pure(lambda x: x * 2),
        ],
        [
            StreamTree.pure(lambda x: x - 3),
            StreamTree.pure(lambda x: x * x),
        ],
    )


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def comonad_functions():
    return [
        lambda t: t.value,
        lambda t: t.children.force().head.value,
        lambda t: (t.value, t.children.force().head.value),
    ]
