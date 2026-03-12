from typeclass.data.writer import Writer
from typeclass.data.sequence import Sequence, Cons, Nil, from_iterable


def values():
    return [
        Writer(Sequence)(10, Nil()),
        Writer(Sequence)(20, Cons("log", Nil())),
        Writer(Sequence)(0, from_iterable("abc")),
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
        Writer(Sequence)((lambda x: x + 1), Nil()),
        Writer(Sequence)((lambda x: x * 2), Cons("f", Nil())),
    ]

def composition_function_values():
    return [
        Writer(Sequence)(lambda x: x + 1, Nil()),
        Writer(Sequence)(lambda x: x * 2, Cons("u", Nil())),
    ], [
        Writer(Sequence)(lambda x: x - 3, Nil()),
        Writer(Sequence)(lambda x: x * x, Cons("v", Nil())),
    ]


def monad_functions():
    return [
        lambda x: Writer(Sequence)(x, Cons("id", Nil())),
        lambda x: Writer(Sequence)(x + 1, Cons("inc", Nil()))
            if isinstance(x, int)
            else Writer(Sequence)(f"{x}!", Cons("bang", Nil())),
        lambda x: Writer(Sequence)(f"[{x}]", Cons("wrap", Nil())),
    ]


def join_values():
    return [
        Writer(Sequence)(
            Writer(Sequence)("x", Nil()),
            Nil(),
        ),
        Writer(Sequence)(
            Writer(Sequence)(10, Cons("inner", Nil())),
            Cons("outer", Nil()),
        ),
        Writer(Sequence)(
            Writer(Sequence)(0, from_iterable("abc")),
            Cons("top", Nil()),
        ),
    ]
