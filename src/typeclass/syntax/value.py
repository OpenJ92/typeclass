from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

A = TypeVar("A")

@dataclass(frozen=True)
class Value(Generic[A]):
    """
    Embed a realized (already interpreted) value into the syntax.

    `Value(x)` is an interpreter barrier: interpreting it yields `x`
    directly, without further interpretation.
    """
    value: A
