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
