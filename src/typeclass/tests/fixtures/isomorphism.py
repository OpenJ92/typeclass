from typeclass.data.either import Left, Right
from typeclass.data.isomorphism import Isomorphism


def inputs():
    return [0, 1, -1, 2, 10]


def pair_inputs():
    return [
        (0, 0),
        (1, 2),
        (-1, 3),
        (10, -5),
    ]


def either_inputs():
    return [
        Left(0),
        Right(0),
        Left(1),
        Right(2),
        Left(-1),
        Right(-5),
        Left(10),
        Right(3),
    ]


def values():
    return [
        Isomorphism(lambda x: x, lambda x: x),
        Isomorphism(lambda x: x + 1, lambda x: x - 1),
        Isomorphism(lambda x: -x, lambda x: -x),
    ]


def triples():
    vals = values()
    return [
        (f, g, h)
        for f in vals
        for g in vals
        for h in vals
    ]


def pairs():
    vals = values()
    return [
        (f, g)
        for f in vals
        for g in vals
    ]


def arrow_functions():
    return [
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: -x,
    ]


def composition_pairs():
    fs = arrow_functions()
    return [
        (f, g)
        for f in fs
        for g in fs
    ]
