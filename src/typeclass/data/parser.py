from __future__ import annotations
from typing import Generic, TypeVar, Callable, Iterable

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.alternative import Alternative
from typeclass.protocols.show import Show
from typeclass.protocols.eq import Eq

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class Parser(Alternative, Applicative[A], Functor[A], Generic[A]):
    def __init__(self, _run: Callable[[str], list[tuple[A, str]]]):
        self._run = _run

    def run(self, input: str) -> list[tuple[A, str]]:
        return self._run(input)

    def fmap(self: Parser[A], f: Callable[[A],B]) -> Parser[B]:
        def inner(input: str) -> list[tuple[B, str]]:
            results = []
            for (a, rest) in  self.run(input):
                results.append((f(a), rest))
            return results
        return Parser(inner)

    @classmethod
    def pure(cls: type, value: A):
        return Parser(lambda input: [(value, input)])

    def ap(self: Parser[Callable[[A],B]], fa: Parser[A]) -> Parser[B]:
        def inner(input: str) -> list[tuple[B, str]]:
            value, results = fa.force(), []
            for (f, left) in self.run(input):
                for (a, right) in value.run(left):
                    results.append((f(a), right))
            return results
        return Parser(inner)

    def empty(cls) -> Parser[A]:
        return Parser(lambda input: [])

    def otherwise(self: Parser[A], other: Parser[A]) -> Parser[A]:
        def inner(input: str):
            left, right = self.run(input), other
            if not left:
                return right.force().run(input)
            return left
        return Parser(inner)
