from typeclass.data.maybe import Just, Nothing


def values():
    return [
        Just(10),
        Nothing(),
    ]


def replacement():
    return "10"
