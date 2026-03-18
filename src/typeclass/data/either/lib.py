from __future__ import annotations

from typing import Callable, TypeVar

from typeclass.data.either.core import Either, Left, Right
from typeclass.runtime.core import evaluated

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")


def _is_left(value: Either[L, R]) -> bool:
    """
    Test whether an Either value is a Left.

    Args:
        value: The Either value to inspect.

    Returns:
        True if `value` is a Left, otherwise False.
    """
    match value:
        case Left():
            return True
    return False
is_left = evaluated(_is_left)


def _is_right(value: Either[L, R]) -> bool:
    """
    Test whether an Either value is a Right.

    Args:
        value: The Either value to inspect.

    Returns:
        True if `value` is a Right, otherwise False.
    """
    match value:
        case Right():
            return True
    return False
is_right = evaluated(_is_right)


def _from_left(default: L, value: Either[L, R]) -> L:
    """
    Extract the Left value, falling back to a default.

    Args:
        default: The value to return if `value` is Right.
        value: The Either value to inspect.

    Returns:
        The contained Left value if present, otherwise `default`.
    """
    match value:
        case Left(value=v):
            return v
        case Right():
            return default
from_left = evaluated(_from_left)


def _from_right(default: R, value: Either[L, R]) -> R:
    """
    Extract the Right value, falling back to a default.

    Args:
        default: The value to return if `value` is Left.
        value: The Either value to inspect.

    Returns:
        The contained Right value if present, otherwise `default`.
    """
    match value:
        case Right(value=v):
            return v
        case Left():
            return default
from_right = evaluated(_from_right)


def _either(
    left_function: Callable[[L], A],
    right_function: Callable[[R], A],
    value: Either[L, R],
) -> A:
    """
    Eliminate an Either by supplying a function for each branch.

    Args:
        left_function: Function applied to a Left value.
        right_function: Function applied to a Right value.
        value: The Either value to inspect.

    Returns:
        The result of applying the appropriate function to the contained value.
    """
    match value:
        case Left(value=v):
            return left_function(v)
        case Right(value=v):
            return right_function(v)
either = evaluated(_either)


def _swap(value: Either[L, R]) -> Either[R, L]:
    """
    Swap the two branches of an Either.

    Args:
        value: The Either value to swap.

    Returns:
        Left(v) if `value` is Right(v), or Right(v) if `value` is Left(v).
    """
    match value:
        case Left(value=v):
            return Right(v)
        case Right(value=v):
            return Left(v)
swap = evaluated(_swap)
