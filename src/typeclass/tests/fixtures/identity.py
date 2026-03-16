from typeclass.data.identity import Identity


def values():
    return [
        Identity(0),
        Identity(1),
        Identity(10),
        Identity(-3),
        Identity("x"),
    ]


def replacement():
    return "z"


def pure_values():
    return [0, 1, 2, 10, -3]


def function_values():
    return [
        Identity(lambda x: x + 1),
        Identity(lambda x: x * 2),
        Identity(lambda x: x - 3),
    ]


def composition_function_values():
    return (
        [
            Identity(lambda x: x + 1),
            Identity(lambda x: x * 2),
        ],
        [
            Identity(lambda x: x - 3),
            Identity(lambda x: x * x),
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
        lambda x: Identity(x + 1),
        lambda x: Identity(x * 2),
        lambda x: Identity(x - 3),
    ]


def join_values():
    return [
        Identity(Identity(0)),
        Identity(Identity(1)),
        Identity(Identity(10)),
    ]


def comonad_functions():
    return [
        lambda w: w.value,
        lambda w: w.value + 1 if isinstance(w.value, int) else w.value,
        lambda w: (w.value, w.value),
    ]
