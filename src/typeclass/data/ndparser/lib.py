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

def eof():
    return NDParser(lambda s: [(None, "")] if s == "" else [])


def one_of(chars):
    return satisfy(lambda c: c in chars)


def none_of(chars):
    return satisfy(lambda c: c not in chars)


def fix(f):
    parser = None

    def inner(s):
        return parser.force().run(s)

    parser = NDParser(inner)
    parser = f(parser)
    return parser


def delay(f):
    return NDParser(lambda s: f().force().run(s))
