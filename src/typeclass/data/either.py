from dataclasses import dataclass
from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")

@dataclass(frozen=True)
class Either(Generic[A, B]):
    pass

@dataclass(frozen=True)
class Left(Either[A, B]):
    value: A

@dataclass(frozen=True)
class Right(Either[A, B]):
    value: B
