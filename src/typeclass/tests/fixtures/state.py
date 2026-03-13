from typeclass.data.state import State


def states():
    return [0, 1, 2, 10, -3]


def values():
    return [
        State(lambda s: (s, s)),
        State(lambda s: (s + 1, s)),
        State(lambda s: (s * 2, s + 1)),
        State(lambda s: (s * s, s - 1)),
    ]


def replacement():
    return "x"


def pure_values():
    return [0, 1, 2, 10]


def function_values():
    return [
        State(lambda s: (lambda x: x + s, s)),
        State(lambda s: (lambda x: x * (s + 1), s + 1)),
    ]


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: State(lambda s: (x + s, s + 1)),
        lambda x: State(lambda s: (x * (s + 1), s + 2)),
        lambda x: State(lambda s: (x - s, s - 1)),
    ]


def join_values():
    return [
        State(lambda s: (State(lambda t: (s + t, t + 1)), s + 1)),
        State(lambda s: (State(lambda t: (s * t, t + 2)), s + 2)),
        State(lambda s: (State(lambda t: (s - t, t - 1)), s - 1)),
    ]
