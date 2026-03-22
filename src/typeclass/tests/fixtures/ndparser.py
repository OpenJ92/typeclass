# tests/fixtures/ndparser.py

from typeclass.data.ndparser import NDParser


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
    Includes both deterministic and nondeterministic cases.
    """
    return [
        NDParser(lambda s: []),
        NDParser(lambda s: [(s[0], s[1:])] if s else []),
        NDParser(lambda s: [(s, "")]),
        NDParser(lambda s: [("ok", s)]),
        NDParser(lambda s: [(s[0], s[1:]), (s[:1], s[1:])] if s else []),
    ]


def consuming_values():
    """
    Parsers safe for some/many.
    They must consume input if they succeed.
    """
    return [
        NDParser(lambda s: [(s[0], s[1:])] if s else []),
        NDParser(lambda s: [(s[:1], s[1:])] if s else []),
        NDParser(lambda s: [(s[0], s[1:]), (s[:1], s[1:])] if s else []),
    ]


def functions():
    return [
        lambda x: NDParser(lambda s: [(f"{x}!", s)]),
        lambda x: NDParser(lambda s: [(f"[{x}]", s)]),
    ]
