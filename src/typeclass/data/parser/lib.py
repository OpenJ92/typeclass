from typeclass.data.sequence import Sequence
from typeclass.data.maybe import Just, Nothing
from typeclass.data.parser import Parser  # adjust import if needed


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

def eof():
    return Parser(lambda s: [(None, "")] if s == "" else [])

def one_of(chars):
    return satisfy(lambda c: c in chars)


def none_of(chars):
    return satisfy(lambda c: c not in chars)


def fix(f):
    parser = None

    def inner(s):
        return parser.force().run(s)

    parser = Parser(inner)
    parser = f(parser)
    return parser


def delay(f):
    return Parser(lambda s: f().force().run(s))
