from typeclass.data.ndparser import NDParser


def item():
    def run(s):
        if not s:
            return []
        return [(s[0], s[1:])]

    return NDParser(run)


def satisfy(pred):
    def run(s):
        if s and pred(s[0]):
            return [(s[0], s[1:])]
        return []

    return NDParser(run)


def char(c):
    return satisfy(lambda x: x == c)


def one_of(chars):
    return satisfy(lambda c: c in chars)


def none_of(chars):
    return satisfy(lambda c: c not in chars)
