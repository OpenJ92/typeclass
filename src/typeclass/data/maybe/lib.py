from typing import Callable, TypeVar

from typeclass.data.maybe.core import Maybe, Just, Nothing
from typeclass.data.sequence import Sequence, Cons, Nil, reverse
from typeclass.typeclasses.symbols import fmap
from typeclass.runtime.core import evaluated

A = TypeVar("A")
B = TypeVar("B")


def _is_just(value: Maybe[A]) -> bool:
    """
    Test whether a Maybe value is a Just.

    Args:
        value: The Maybe value to inspect.

    Returns:
        True if `value` is a Just, otherwise False.
    """
    match value:
        case Just():
            return True
    return False
is_just = evaluated(_is_just)


def _is_nothing(value: Maybe[A]) -> bool:
    """
    Test whether a Maybe value is Nothing.

    Args:
        value: The Maybe value to inspect.

    Returns:
        True if `value` is Nothing, otherwise False.
    """
    match value:
        case Nothing():
            return True
    return False
is_nothing = evaluated(_is_nothing)


def _from_maybe(default: A, value: Maybe[A]) -> A:
    """
    Extract the value from a Maybe, falling back to a default.

    Args:
        default: The value to return if `value` is Nothing.
        value: The Maybe value to inspect.

    Returns:
        The contained value if `value` is Just, otherwise `default`.
    """
    match value:
        case Just(value=v):
            return v
        case Nothing():
            return default
from_maybe = evaluated(_from_maybe)


def _maybe(default: B, function: Callable[[A], B], value: Maybe[A]) -> B:
    """
    Eliminate a Maybe by supplying a default and a function.

    Args:
        default: The result to return if `value` is Nothing.
        function: The function to apply if `value` is Just.
        value: The Maybe value to inspect.

    Returns:
        `default` if `value` is Nothing, otherwise `function` applied to
        the contained value.
    """
    match value:
        case Just(value=v):
            return function(v)
        case Nothing():
            return default
maybe = evaluated(_maybe)


def _cat_maybes(values: Sequence[Maybe[A]]) -> Sequence[A]:
    """
    Collect all present values from a list of Maybe values.

    Args:
        values: A list of Maybe values.

    Returns:
        A list containing the values from every Just in order.
    """
    cur = values
    out: Sequence[A] = Nil()

    while isinstance(cur, Cons):
        match cur.head:
            case Just(value=value):
                out = Cons(value, out)
        cur = cur.tail

    return reverse(out)
cat_maybes = evaluated(_cat_maybes)


def _map_maybe(function: Callable[[A], Maybe[B]], values: Sequence[A]) -> Sequence[B]:
    """
    Map a partial function over a list, keeping only present results.

    Args:
        function: A function from A to Maybe[B].
        values: The input values.

    Returns:
        A list containing the values from every Just result.
    """
    return cat_maybes(values |fmap| function)
map_maybe  = evaluated(_map_maybe)
