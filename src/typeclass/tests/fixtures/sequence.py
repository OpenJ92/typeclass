from typeclass.data.sequence import Sequence


def empty():
    return Sequence(())


def singleton():
    return Sequence((10,))


def small():
    return Sequence((1, 2, 3))


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
        Sequence((lambda x: x + 1,)),
        Sequence((lambda x: x * 2,)),
        Sequence(()),
    ]


def composition_function_values():
    return [
        Sequence((lambda x: x + 1,)),
        Sequence((lambda x: x * 2,)),
        Sequence(()),
    ], [
        Sequence((lambda x: x - 3,)),
        Sequence((lambda x: x * x,)),
        Sequence(()),
    ]


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: Sequence((x,)),
        lambda x: Sequence((x, x + 1)),
        lambda x: Sequence(()) if x == 0 else Sequence((x - 1,)),
    ]


def join_values():
    return [
        Sequence(()),
        Sequence((Sequence(()),)),
        Sequence((Sequence((1,)),)),
        Sequence((Sequence((1, 2)), Sequence((3,)))),
    ]


def triples():
    xs = values()
    return [
        (x, y, z)
        for x in xs
        for y in xs
        for z in xs
    ]
