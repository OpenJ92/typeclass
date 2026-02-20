# typeclass/protocols/eq.py

from typing import Protocol

class Eq(Protocol):
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

