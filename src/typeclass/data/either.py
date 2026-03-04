from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")

class Either(Generic[A, B]):
    pass

class Left(Either[A, B]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self):
        return f"Left({self.value})"

class Right(Either[A, B]):
    def __init__(self, value: B):
        self.value = value

    def __repr__(self):
        return f"Right({self.value})"
