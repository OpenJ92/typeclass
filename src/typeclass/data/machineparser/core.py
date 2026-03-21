from dataclasses import dataclass
from typing import Any, Callable

from typeclass.data.thunk import delay
from typeclass.typeclasses.functor import Map
from typeclass.typeclasses.applicative import Pure, Ap
from typeclass.typeclasses.alternative import Empty, Otherwise, Many, Some
from typeclass.typeclasses.monad import Bind


Predicate = Callable[[Any], bool]


@dataclass(frozen=True)
class Satisfy:
    predicate: Predicate

    def __repr__(self) -> str:
        return f"Satisfy({self.predicate!r})"


@dataclass(frozen=True)
class MachineParser:
    expr: Any

    def fmap(self, f: Callable[[Any], Any]) -> MachineParser:
        return MachineParser(Map(delay(f), delay(self.expr)))

    @classmethod
    def pure(cls, value: Any) -> MachineParser:
        return MachineParser(Pure(cls, delay(value)))

    @classmethod
    def empty(cls) -> MachineParser:
        return MachineParser(Empty(cls))

    def ap(self, value: MachineParser) -> MachineParser:
        if not isinstance(value, MachineParser):
            raise TypeError(
                f"MachineParser.ap expected MachineParser, got {type(value)!r}"
            )
        return MachineParser(Ap(delay(self.expr), delay(value.expr)))

    def otherwise(self, other: MachineParser) -> MachineParser:
        if not isinstance(other, MachineParser):
            raise TypeError(
                f"MachineParser.otherwise expected MachineParser, got {type(other)!r}"
            )
        return MachineParser(Otherwise(delay(self.expr), delay(other.expr)))

    def bind(self, f: Callable[[Any], MachineParser]) -> MachineParser:
        def k(a: Any):
            out = f(a)
            if not isinstance(out, MachineParser):
                raise TypeError(
                    "MachineParser.bind continuation must return MachineParser, "
                    f"got {type(out)!r}"
                )
            return out.expr

        return MachineParser(Bind(delay(self.expr), delay(k)))

    def many(self) -> MachineParser:
        return MachineParser(Many(MachineParser, delay(self.expr)))

    def some(self) -> MachineParser:
        return MachineParser(Some(MachineParser, delay(self.expr)))

    def run(self, tokens: Any) -> list[tuple[Any, Any]]:
        from typeclass.interpret.parser import run_parser_machine
        return run_parser_machine(self.expr, tokens)

    def run_recursive(self, tokens: Any) -> list[tuple[Any, Any]]:
        from typeclass.interpret.parser import run_parser_recursive
        return run_parser_recursive(self.expr, tokens)

    def __repr__(self) -> str:
        return f"MachineParser({self.expr!r})"


def satisfy(predicate: Predicate) -> MachineParser:
    return MachineParser(Satisfy(predicate))


def token(expected: Any) -> MachineParser:
    return satisfy(lambda actual: actual == expected)
