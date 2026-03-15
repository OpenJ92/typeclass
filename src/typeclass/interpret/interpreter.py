from typeclass.syntax.value import Value
from typeclass.syntax.functor import Map 
from typeclass.syntax.applicative import Ap, Pure
from typeclass.syntax.alternative import Otherwise, Empty, Some, Many
from typeclass.syntax.monad import Bind, Return
from typeclass.syntax.comonad import Extract, Duplicate
from typeclass.syntax.semigroupoid import Compose
from typeclass.syntax.category import ID
from typeclass.syntax.groupoid import Invert
from typeclass.syntax.semigroup import Combine
from typeclass.syntax.monoid import MEmpty
from typeclass.syntax.group import Inverse
from typeclass.syntax.arrow import Arr, First, Second, Split, Fanout
from typeclass.syntax.arrowchoice import Left, Right, PlusPlus, OrOr
from typeclass.syntax.arrowapply import Apply

from typeclass.data.either import Left as ELeft, Right as ERight
from typeclass.data.thunk import Thunk

from functools import wraps
from inspect import signature

def realize(expression):
    return interpret(expression, None, None)
def evaluate(expression):
    return realize(expression).force()
def curry(fn):
    arity = len(signature(fn).parameters)

    @wraps(fn)
    def curried(*args):
        if len(args) >= arity:
            return fn(*args)
        return lambda *more: curried(*(args + more))
    return curried
def interpreted(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return fn(
            *[realize(a) for a in args],
            **{k: realize(v) for k, v in kwargs.items()},
        )
    return wrapped


def evaluated(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return fn(
            *[evaluate(a) for a in args],
            **{k: evaluate(v) for k, v in kwargs.items()},
        )
    return wrapped

def interpret(free, cofree, env):
    """
    Normalize a syntax tree into a delayed runtime value.

    The interpreter evaluates nodes of the free syntax language and dispatches
    them to the corresponding runtime typeclass implementations.

    Execution model:

        syntax node
        → interpreter pattern match
        → runtime method call
        → possibly another syntax expression
        → interpreter normalization
        → runtime value

    The interpreter is therefore *re-entrant*: implementation methods may return
    either concrete runtime values or further syntax expressions. The interpreter
    repeatedly normalizes until a realized value is obtained.

    All results are returned wrapped in `Thunk` so evaluation remains delayed
    until the final `.force()` boundary.

    Parameters
    ----------
    free:
        The syntax node being interpreted.

    cofree:
        Reserved for future extensions (e.g. annotated syntax trees).

    env:
        Reserved for environment-based interpreters.

    Returns
    -------
    Thunk
        A delayed runtime value.
    """

    match free:

        # ----- Functor ---------------------------------------------------------
        # Implements fmap by interpreting both the function and value, then
        # delegating to the runtime Functor implementation.

        case Map(function, value):
            value = interpret(value.force(), None, None).force()
            function = interpret(function.force(), None, None)

            def k(a):
                return interpret(function.force()(a), None, None).force()

            return Thunk(lambda: value.fmap(Thunk(lambda: k)))

        # ----- Applicative -----------------------------------------------------
        # Implements fmap by interpreting both the function and value, then
        # delegating to the runtime Functor implementation.
            
        case Pure(cls, value):
            value = interpret(value.force(), None, None).force()
            return Thunk(lambda: cls.pure(value))

        case Ap(function, value):
            function = interpret(function.force(), None, None).force()
            value    = interpret(value.force(), None, None)
            return Thunk(lambda: function.ap(value))

        # ----- Alternative -----------------------------------------------------
        # Implements empty, otherwise, and the derived combinators some/many.
        # some/many are lowered into pure/ap/otherwise expressions.

        case Empty(cls):
            return Thunk(lambda: cls.empty())

        case Otherwise(alter, native):
            alter  = interpret(alter.force(), None, None).force()
            native = interpret(native.force(), None, None)
            return Thunk(lambda: alter.otherwise(native))
        
        case Many(cls, value):
            some = Thunk(lambda: Some(cls, value))
            pure = Thunk(lambda: Pure(cls, Thunk(lambda: [])))
            otherwise = Otherwise(some, pure)
            return Thunk(lambda: interpret(otherwise, None, None).force())

        case Some(cls, value):
            cons = Thunk(lambda: (lambda x: (lambda xs: [x] + xs)))
            _map  = Thunk(lambda: Map(cons, value))
            many = Thunk(lambda: Many(cls, value))
            ap   = Ap(_map, many)
            return Thunk(lambda: interpret(ap, None, None).force())

        # ----- Monad -----------------------------------------------------------
        # Implements empty, otherwise, and the derived combinators some/many.
        # some/many are lowered into pure/ap/otherwise expressions.

        case Return(cls, value):
            value = interpret(value.force(), None, None).force()
            return Thunk(lambda: cls.pure(value))

        case Bind(ma, f):
            ma = interpret(ma.force(), None, None).force()
            f = interpret(f.force(), None, None)

            def k(a):
                return interpret(f.force()(a), None, None).force()

            return Thunk(lambda: ma.bind(Thunk(lambda: k)))

        # ----- Comonad ---------------------------------------------------------
        # Core Comonad operations. `extend` is derived and lowered through
        # `duplicate` and `fmap`, so only extract and duplicate are primitive.

        case Extract(wa):
            wa = interpret(wa.force(), None, None).force()
            return Thunk(lambda: wa.extract())

        case Duplicate(wa):
            wa = interpret(wa.force(), None, None).force()
            return Thunk(lambda: wa.duplicate())

        # ----- Semigroupoid -----------------------------------------------------
        # Sequential composition of morphisms.

        case Compose(fbc, fab):
            fbc = interpret(fbc.force(), None, None).force()
            fab = interpret(fab.force(), None, None)

            return Thunk(lambda: fbc.compose(fab))

        # ----- Category ---------------------------------------------------------
        # Identity morphism.

        case ID(cls):
            return Thunk(lambda: cls.id())

        # ----- Groupoid ---------------------------------------------------------
        # Identity morphism.

        case Invert(fab):
            fab = interpret(fab.force(), None, None).force()
            return Thunk(lambda: fab.invert())

        # ----- Semigroup --------------------------------------------------------
        # Binary associative combination.

        case Combine(a, b):
            a = interpret(a.force(), None, None).force()
            b = interpret(b.force(), None, None)

            return Thunk(lambda: a.combine(b))

        # ----- Monoid -----------------------------------------------------------
        # Identity element for a Semigroup.

        case MEmpty(cls):
            return Thunk(lambda: cls.mempty())

        # ----- Group ------------------------------------------------------------
        # Inversion operation for Group structures.

        case Inverse(fab):
            fab = interpret(fab.force(), None, None).force()

            return Thunk(lambda: fab.inverse())

        # ----- Arrow ------------------------------------------------------------
        # Core Arrow operations and derived combinators expressed in terms of
        # arr and first. Derived operations are lowered into simpler Arrow
        # expressions and reinterpreted.

        case Arr(cls, fab):
            def k(a):
                return interpret(fab.force(), None, None).force()(a)
            return Thunk(lambda: cls.arrow(Thunk(lambda: k)))

        case First(cls, aab):
            def k(a):
                return interpret(aab.force(), None, None).force()(a)
            return Thunk(lambda: cls.first(Thunk(lambda: k)))

        case Second(cls, aab):
            def swap(pair):
                x, y = pair
                return (y, x)

            arrswap = Thunk(lambda: Arr(cls, Thunk(lambda: swap)))
            first   = Thunk(lambda: First(cls, aab))

            one  = Thunk(lambda: Compose(first, arrswap))
            comp = Compose(arrswap, one)

            return Thunk(lambda: interpret(comp, None, None).force())

        case Split(cls, aab, acd):
            first_  = Thunk(lambda: First(cls, aab))
            second_ = Thunk(lambda: Second(cls, acd))

            comp = Compose(second_, first_)
            return Thunk(lambda: interpret(comp, None, None).force())

        case Fanout(cls, aab, aac):
            def duplicate(a):
                return (a, a)
            
            arrduplicate = Thunk(lambda: Arr(cls, Thunk(lambda: duplicate)))
            split = Thunk(lambda: Split(cls, aab, aac))
            comp = Compose(split, arrduplicate)

            return Thunk(lambda: interpret(comp, None, None).force())

        # ----- ArrowChoice  -----------------------------------------------------
        # Core Arrow operations and derived combinators expressed in terms of
        # arr and first. Derived operations are lowered into simpler Arrow
        # expressions and reinterpreted.

        case Left(cls, aab):
            def k(a):
                return interpret(aab.force(), None, None).force()(a)
            return Thunk(lambda: cls.left(Thunk(lambda: k)))

        case Right(cls, aab):
            def swap(e):
                match e:
                    case ELeft(x):
                        return ERight(x)
                    case ERight(x):
                        return ELeft(x)

            arrswap = Thunk(lambda: Arr(cls, Thunk(lambda: swap)))
            left_   = Thunk(lambda: Left(cls, aab))

            one  = Thunk(lambda: Compose(left_, arrswap))
            comp = Compose(arrswap, one)

            return Thunk(lambda: interpret(comp, None, None).force())

        case PlusPlus(cls, aab, acd):
            left_  = Thunk(lambda: Left(cls, aab))
            right_ = Thunk(lambda: Right(cls, acd))
            comp   = Compose(right_, left_)
            return Thunk(lambda: interpret(comp, None, None).force())

        case OrOr(cls, aab, acb):
            def merge(e):
                match e:
                    case ELeft(b):
                        return b
                    case ERight(b):
                        return b

            ppg = Thunk(lambda: PlusPlus(cls, aab, acb))
            arrmerge = Thunk(lambda: Arr(cls, Thunk(lambda: merge)))

            comp = Compose(arrmerge, ppg)
            return Thunk(lambda: interpret(comp, None, None).force())

        # ----- ArrowApply  -----------------------------------------------------
        # Dynamic arrow application. Allows an arrow produced at runtime to be
        # immediately applied.

        case Apply(cls):
            return Thunk(lambda: interpret(cls.app(), None, None).force())

        # ----- Base ------------------------------------------------------------
        # Base case: already a runtime value.

        case _:
            return Thunk(lambda: free)
