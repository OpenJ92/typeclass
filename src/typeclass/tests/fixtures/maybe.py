from typeclass.data.maybe import Just, Nothing


def values():
    return [
        Just(10),
        Just(0),
        Nothing(),
    ]


def replacement():
    return "10"


def pure_values():
    return [
        0,
        1,
        10,
    ]


def function_values():
    return [
        Just(lambda x: x + 1),
        Just(lambda x: x * 2),
        Nothing(),
    ]


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: Just(x + 1),
        lambda x: Just(x * 2),
        lambda x: Nothing() if x == 0 else Just(x - 1),
    ]


def join_values():
    return [
        Just(Just(10)),
        Just(Just(0)),
        Just(Nothing()),
        Nothing(),
    ]
