from typeclass.data.stream import repeat, iterate


def naturals_from_zero():
    return iterate(lambda x: x + 1, 0)


def ones():
    return repeat(1)


def evens():
    return iterate(lambda x: x + 2, 0)


def values():
    return [
        naturals_from_zero(),
        ones(),
        evens(),
    ]


def replacement():
    return "x"


def pure_values():
    return [0, 1, 10]


def function_values():
    return [
        repeat(lambda x: x + 1),
        repeat(lambda x: x * 2),
    ]


def composition_function_values():
    return (
        [
            repeat(lambda x: x + 1),
            repeat(lambda x: x * 2),
        ],
        [
            repeat(lambda x: x - 3),
            repeat(lambda x: x * x),
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
        lambda s: s.head,
        lambda s: s.head + s.tail.force().head,
        lambda s: (s.head, s.tail.force().head),
    ]
