from typeclass.data.writer import Writer


def values():
    return [
        Writer(10, ""),
        Writer(20, "log"),
        Writer(0, "abc"),
    ]


def replacement():
    return "x"
