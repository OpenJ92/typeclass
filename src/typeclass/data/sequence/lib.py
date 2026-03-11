from typeclass.data.sequence.core import Sequence, Cons, Nil, concat

def from_iterable(iterable):
    """
    Construct a Sequence from any iterable.
    
    Elements are inserted in the same order as the iterable.
    """
    result = Nil()
    for x in reversed(list(iterable)):
        result = Cons(x, result)
    return result

def length(xs: Sequence[A]) -> int:
    match xs:
        case Cons(_, ys):
            return 1 + length(ys)
        case _:
            return 0

def zipwith(function: Callable[[A, B], C], xs: Sequence[A], ys: Sequence[B]) -> Sequence[C]:
    match (xs, ys):
        case (Cons(x, xss), Cons(y, yss)):
            return Cons(function(x, y), zipwith(function, xss, yss))
        case _:
            return Nil()
            
