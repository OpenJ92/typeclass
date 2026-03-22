from typing import Generic, TypeVar, Callable, Iterable

from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.alternative import Alternative
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.eq import Eq

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Parser(Monad, Alternative, Applicative[A], Functor[A], Generic[A]):
    def __init__(self, _run: Callable[[str], list[tuple[A, str]]]):
        self._run = _run

    def run(self, tokens: str) -> list[tuple[A, str]]:
        return self._run(tokens)

    # --- Functor -----------------------------------------------------------

    def fmap(self: Parser[A], f: Callable[[A],B]) -> Parser[B]:
        def inner(tokens: str) -> list[tuple[B, str]]:
            results = []
            for (a, rest) in  self.run(tokens):
                results.append((f.force()(a), rest))
            return results
        return Parser(inner)

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls: type, value: A):
        return Parser(lambda tokens: [(value, tokens)])

    def ap(self: Parser[Callable[[A],B]], fa: Parser[A]) -> Parser[B]:
        def inner(tokens: str) -> list[tuple[B, str]]:
            value, results = fa.force(), []
            for (f, left) in self.run(tokens):
                for (a, right) in value.run(left):
                    results.append((f(a), right))
            return results
        return Parser(inner)

    # --- Alternative -------------------------------------------------------

    @classmethod
    def empty(cls) -> Parser[A]:
        return Parser(lambda tokens: [])

    def otherwise(self: Parser[A], other: Parser[A]) -> Parser[A]:
        def inner(tokens: str):
            left, right = self.run(tokens), other
            if not left:
                return right.force().run(tokens)
            return left
        return Parser(inner)

    @classmethod
    def _repeat_maximal(cls, parser: "Parser[A]", input: str) -> list[tuple[list[A], str]]:
        out: list[tuple[list[A], str]] = []
        stack: list[tuple[list[A], str]] = []
    
        seeds: list[tuple[list[A], str]] = []
        for (a, rest) in parser.force().run(input):
            if rest == input:
                continue
            seeds.append(([a], rest))
    
        for item in reversed(seeds):
            stack.append(item)
    
        while stack:
            xs, current = stack.pop()
    
            nexts: list[tuple[list[A], str]] = []
            for (a, rest) in parser.force().run(current):
                if rest == current:
                    continue
                nexts.append((xs + [a], rest))
    
            if nexts:
                for item in reversed(nexts):
                    stack.append(item)
            else:
                out.append((xs, current))
    
        return out

    @classmethod
    def some(cls, parser: "Parser[A]") -> "Parser[list[A]]":
        def inner(input: str) -> list[tuple[list[A], str]]:
            return cls._repeat_maximal(parser, input)
        return cls(inner)
    
    
    @classmethod
    def many(cls, parser: "Parser[A]") -> "Parser[list[A]]":
        def inner(input: str) -> list[tuple[list[A], str]]:
            out = cls._repeat_maximal(parser, input)
            if out:
                return out
            return [([], input)]
        return cls(inner)

    # --- Monad -------------------------------------------------------------

    def bind(self: Parser[A], fm: Callable[[A], Parser[B]]) -> Parser[B]:
        def inner(tokens: str) -> list[tuple[A, str]]:
            _fm, results = fm.force(), []
            for (a, left) in self.run(tokens):
                for (b, right) in _fm(a).run(left):
                    results.append((b, right))
            return results
        return Parser(inner)
