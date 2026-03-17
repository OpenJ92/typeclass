from typeclass.data.writer import Writer
from typeclass.data.sequence import Sequence


def values():
    return [
        Writer(Sequence)(10, Sequence(())),
        Writer(Sequence)(20, Sequence(("log",))),
        Writer(Sequence)(0, Sequence(tuple("abc"))),
    ]


def pure_values():
    return [
        0,
        1,
        10,
    ]


def replacement():
    return "x"


def function_values():
    return [
        Writer(Sequence)((lambda x: x + 1), Sequence(())),
        Writer(Sequence)((lambda x: x * 2), Sequence(("f",))),
    ]


def composition_function_values():
    return [
        Writer(Sequence)(lambda x: x + 1, Sequence(())),
        Writer(Sequence)(lambda x: x * 2, Sequence(("u",))),
    ], [
        Writer(Sequence)(lambda x: x - 3, Sequence(())),
        Writer(Sequence)(lambda x: x * x, Sequence(("v",))),
    ]


def monad_functions():
    return [
        lambda x: Writer(Sequence)(x, Sequence(("id",))),
        lambda x: Writer(Sequence)(x + 1, Sequence(("inc",)))
            if isinstance(x, int)
            else Writer(Sequence)(f"{x}!", Sequence(("bang",))),
        lambda x: Writer(Sequence)(f"[{x}]", Sequence(("wrap",))),
    ]


def join_values():
    return [
        Writer(Sequence)(
            Writer(Sequence)("x", Sequence(())),
            Sequence(()),
        ),
        Writer(Sequence)(
            Writer(Sequence)(10, Sequence(("inner",))),
            Sequence(("outer",)),
        ),
        Writer(Sequence)(
            Writer(Sequence)(0, Sequence(tuple("abc"))),
            Sequence(("top",)),
        ),
    ]
