# tests/fixtures/reader.py

from typeclass.data.reader import Reader


def envs():
    return [0, 1, 2, 10, -3]


def values():
    return [
        Reader(lambda r: r),
        Reader(lambda r: r + 1),
        Reader(lambda r: r * 2),
        Reader(lambda r: r * r),
    ]


def replacement():
    return "x"


def pure_values():
    return [0, 1, 2, 10]


def function_values():
    return [
        Reader(lambda r: (lambda x: x + r)),
        Reader(lambda r: (lambda x: x * (r + 1))),
    ]


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: Reader(lambda r: x + r),
        lambda x: Reader(lambda r: x * (r + 1)),
        lambda x: Reader(lambda r: x - r),
    ]


def join_values():
    return [
        Reader(lambda r: Reader(lambda s: r + s)),
        Reader(lambda r: Reader(lambda s: r * s)),
        Reader(lambda r: Reader(lambda s: r - s)),
    ]
