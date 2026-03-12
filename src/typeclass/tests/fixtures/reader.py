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
