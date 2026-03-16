from typing import Protocol, TypeVar

T = TypeVar("T")


class Force(Protocol[T]):
    """
    Force[T] is the interface for delayed values that can be realized
    into a value of type T.

    This is used in protocol and data method signatures to describe the
    runtime contract seen by implementations:

        - syntax/operator layer accepts ordinary Python values
        - syntax nodes wrap those values into delayed forms
        - interpreter passes delayed arguments into implementations
        - implementations call .force() to realize the semantic value

    Any concrete delayed wrapper (for example Thunk[T]) satisfies this
    protocol structurally as long as it defines:

        force(self) -> T
    """

    def force(self) -> T: ...
