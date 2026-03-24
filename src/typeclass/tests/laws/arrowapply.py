from typing import Callable, TypeVar

from typeclass.typeclasses.arrowapply import ArrowApply
from typeclass.typeclasses.symbols import arrow, app

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def arrowapply_arr_app_expr(
    witness: type[ArrowApply[A, B]],
    f: Callable[[A], B],
):
    """
    ArrowApply law:
        app ∘ arr(lambda a: (arr(f), a)) == arr(f)
        arr(lambda a: (arr(f), a)) >>> app == arr(f)

    In your syntax:
        arr(lambda a: (arr(f), a)) >>> app == arr(f)
    """
    lhs = (witness |arrow| (lambda a: ((witness |arrow| f), a))) \
        |rcompose| apply(witness) 
    rhs = witness |arrow| f
    return lhs, rhs
