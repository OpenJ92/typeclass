from typeclass.data.sequence import Sequence
from typeclass.data.maybe import Just, Nothing
from typeclass.data.parser import Parser  # adjust import if needed


# --- core primitives ----------------------------------------------------------


def item():
    def run(s):
        if not s:
            return Sequence(())
        return Sequence(((s[0], s[1:]),))
    return Parser(run)


def satisfy(pred):
    def run(s):
        if s and pred(s[0]):
            return Sequence(((s[0], s[1:]),))
        return Sequence(())
    return Parser(run)


def char(c):
    return satisfy(lambda x: x == c)


# --- derived combinators ------------------------------------------------------

def one_of(chars):
    return satisfy(lambda c: c in chars)


def none_of(chars):
    return satisfy(lambda c: c not in chars)
