from typing import Generic, TypeVar, Callable
from collections import deque

from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.alternative import Alternative
from typeclass.typeclasses.monad import Monad

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class NDParser(Monad, Alternative, Applicative[A], Functor[A], Generic[A]):
    def __init__(self, _run: Callable[[str], list[tuple[A, str]]]):
        self._run = _run

    def run(self, tokens: str) -> list[tuple[A, str]]:
        return self._run(tokens)

    # --- Functor -----------------------------------------------------------

    def fmap(self: NDParser[A], f: Callable[[A], B]) -> NDParser[B]:
        def inner(tokens: str) -> list[tuple[B, str]]:
            results = []
            for (a, rest) in self.run(tokens):
                results.append((f.force()(a), rest))
            return results

        return NDParser(inner)

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls, value: A) -> NDParser[A]:
        return cls(lambda tokens: [(value, tokens)])

    def ap(self: NDParser[Callable[[A], B]], fa: NDParser[A]) -> NDParser[B]:
        def inner(tokens: str) -> list[tuple[B, str]]:
            value = fa.force()
            results: list[tuple[B, str]] = []

            for (f, left) in self.run(tokens):
                for (a, right) in value.run(left):
                    results.append((f(a), right))

            return results

        return NDParser(inner)

    # --- Alternative -------------------------------------------------------

    @classmethod
    def empty(cls) -> NDParser[A]:
        return cls(lambda tokens: [])

    def otherwise(self: NDParser[A], other: NDParser[A]) -> NDParser[A]:
        def inner(tokens: str) -> list[tuple[A, str]]:
            left = self.run(tokens)
            right = other.force().run(tokens)
            return left + right

        return NDParser(inner)
    
    @classmethod
    def _repeat_all(cls, parser: NDParser[A], input: str) -> list[tuple[list[A], str]]:
        out: deque[tuple[list[A], str]] = deque()
        stack: deque[tuple[list[A], str]] = deque()
    
        for (a, rest) in parser.force().run(input):
            if rest == input:
                continue
            stack.append(([a], rest))
    
        while stack:
            xs, current = stack.popleft()
            out.appendleft((xs, current))
    
            nexts: deque[tuple[list[A], str]] = deque()
            for (a, rest) in parser.force().run(current):
                if rest == current:
                    continue
                nexts.appendleft((xs + [a], rest))
    
            stack.extendleft(nexts)
    
        return list(out)

    @classmethod
    def some(cls, parser: NDParser[A]) -> NDParser[list[A]]:
        def inner(input: str) -> list[tuple[list[A], str]]:
            return cls._repeat_all(parser, input)

        return cls(inner)

    @classmethod
    def many(cls, parser: NDParser[A]) -> NDParser[list[A]]:
        def inner(input: str) -> list[tuple[list[A], str]]:
            # fully nondeterministic many = pure([]) ∪ some(parser)
            return cls._repeat_all(parser, input) + [([], input)] 

        return cls(inner)

    # --- Monad -------------------------------------------------------------

    def bind(self: NDParser[A], fm: Callable[[A], NDParser[B]]) -> NDParser[B]:
        def inner(tokens: str) -> list[tuple[B, str]]:
            _fm = fm.force()
            results: list[tuple[B, str]] = []

            for (a, left) in self.run(tokens):
                for (b, right) in _fm(a).run(left):
                    results.append((b, right))

            return results

        return NDParser(inner)
