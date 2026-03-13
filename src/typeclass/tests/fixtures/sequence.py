from typeclass.data.sequence import Nil, Cons


def empty():
    return Nil()


def singleton():
    return Cons(10, Nil())


def small():
    return Cons(1, Cons(2, Cons(3, Nil())))


def values():
    return [
        empty(),
        singleton(),
        small(),
    ]


def replacement():
    return "x"


def pure_values():
    return [
        0,
        1,
        10,
    ]


def function_values():
    return [
        Cons(lambda x: x + 1, Nil()),
        Cons(lambda x: x * 2, Nil()),
        Nil(),
    ]


def composition_function_values():
    return [
        Cons(lambda x: x + 1, Nil()),
        Cons(lambda x: x * 2, Nil()),
        Nil(),
    ], [
        Cons(lambda x: x - 3, Nil()),
        Cons(lambda x: x * x, Nil()),
        Nil(),
    ]


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: Cons(x, Nil()),
        lambda x: Cons(x, Cons(x + 1, Nil())),
        lambda x: Nil() if x == 0 else Cons(x - 1, Nil()),
    ]


def join_values():
    return [
        Nil(),
        Cons(Nil(), Nil()),
        Cons(Cons(1, Nil()), Nil()),
        Cons(Cons(1, Cons(2, Nil())), Cons(Cons(3, Nil()), Nil())),
    ]

def triples():
    xs = values()
    return [
        (x, y, z)
        for x in xs
        for y in xs
        for z in xs
    ]
