from typing import Protocol

class Show(Protocol):
    def __repr__(self) -> str:
        raise NotImplementedError
