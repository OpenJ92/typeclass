# tests/fixtures/parser.py

from typeclass.data.parser import Parser


def inputs():
    return [
        "",
        "a",
        "ab",
        "abc",
        "1",
        "42xyz",
    ]


def values():
    """
    General parsers used across Functor, Applicative, Monad, Alternative tests.
    """
    return [
        Parser(lambda s: []),
        Parser(lambda s: [(s[0], s[1:])] if s else []),
        Parser(lambda s: [(s, "")]),
        Parser(lambda s: [("ok", s)]),
    ]


def consuming_values():
    """
    Parsers safe for some/many.
    They must consume input if they succeed.
    """
    return [
        Parser(lambda s: [(s[0], s[1:])] if s else []),
        Parser(lambda s: [(s[:1], s[1:])] if s else []),
    ]


def functions():
    return [
        lambda x: Parser(lambda s: [(f"{x}!", s)]),
        lambda x: Parser(lambda s: [(f"[{x}]", s)]),
    ]
