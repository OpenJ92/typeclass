from typeclass.data.either import Left, Right


def left_values():
    return [
        Left("a"),
        Left("b"),
        Left("boom"),
    ]


def right_values():
    return [
        Right(0),
        Right(1),
        Right(10),
        Right(-3),
    ]


def values():
    return left_values() + right_values()


def pure_values():
    return [0, 1, 2, 10, -3]


def replacement():
    return "z"


def function_values():
    return [
        Right(lambda x: x + 1),
        Right(lambda x: x * 2),
        Right(lambda x: x - 3),
        Left("no function"),
    ]


def composition_function_values():
    return (
        [
            Right(lambda x: x + 1),
            Right(lambda x: x * 2),
            Left("u-left"),
        ],
        [
            Right(lambda x: x - 3),
            Right(lambda x: x * x),
            Left("v-left"),
        ],
    )


def binary_functions():
    return [
        lambda a, b: (a, b),
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]


def monad_functions():
    return [
        lambda x: Right(x + 1),
        lambda x: Right(x * 2),
        lambda x: Right(x - 3),
        lambda x: Left(f"bad:{x}"),
    ]


def join_values():
    return [
        Right(Right(0)),
        Right(Right(1)),
        Right(Left("inner-left")),
        Left("outer-left"),
    ]
