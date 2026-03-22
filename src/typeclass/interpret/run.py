from typeclass.typeclasses.functor import Map 
from typeclass.typeclasses.applicative import Ap, Pure
from typeclass.typeclasses.alternative import Otherwise, Empty, Some, Many
from typeclass.typeclasses.monad import Bind, Return
from typeclass.typeclasses.comonad import Extract, Duplicate
from typeclass.typeclasses.semigroupoid import Compose
from typeclass.typeclasses.category import ID
from typeclass.typeclasses.groupoid import Invert
from typeclass.typeclasses.semigroup import Combine
from typeclass.typeclasses.monoid import MEmpty
from typeclass.typeclasses.group import Inverse
from typeclass.typeclasses.arrow import Arr, First, Second, Split, Fanout
from typeclass.typeclasses.arrowchoice import Left, Right, PlusPlus, OrOr
from typeclass.typeclasses.arrowapply import Apply

from typeclass.data.either import Left as ELeft, Right as ERight
from typeclass.data.thunk import Thunk, suspend, delay, resume

def interpret(expression):
    return run(expression, None, None)

def evaluate(expression):
    return interpret(expression).force()

def run(free, cofree, env):
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
        The syntax node being runed.

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
        # Implements fmap by runing both the function and value, then
        # delegating to the runtime Functor implementation.

        case Map(function, value):
            value = run(value.force(), cofree, env).force()
            function = run(function.force(), cofree, env)

            def k(a):
                return run(function.force()(a), cofree, env).force()

            return suspend(value.fmap, delay(k))

        # ----- Applicative -----------------------------------------------------
        # Implements fmap by runing both the function and value, then
        # delegating to the runtime Functor implementation.
            
        case Pure(cls, value):
            value = run(value.force(), cofree, env).force()
            return suspend(cls.pure, value)

        case Ap(function, value):
            function = run(function.force(), cofree, env).force()
            value    = run(value.force(), cofree, env)
            return suspend(function.ap, value)

        # ----- Alternative -----------------------------------------------------
        # Implements empty, otherwise, and the derived combinators some/many.
        # some/many are lowered into pure/ap/otherwise expressions.

        case Empty(cls):
            return suspend(cls.empty)

        case Otherwise(alter, native):
            alter  = run(alter.force(), cofree, env).force()
            native = run(native.force(), cofree, env)
            return suspend(alter.otherwise, native)
        
        case Many(cls, value):
            value = run(value.force(), None, None)
            return suspend(cls.many, value)

        case Some(cls, value):
            value = run(value.force(), None, None)
            return suspend(cls.some, value)

        # ----- Monad -----------------------------------------------------------
        # Implements empty, otherwise, and the derived combinators some/many.
        # some/many are lowered into pure/ap/otherwise expressions.

        case Return(cls, value):
            value = run(value.force(), cofree, env).force()
            return suspend(cls.pure, value)

        case Bind(ma, f):
            ma = run(ma.force(), cofree, env).force()
            f = run(f.force(), cofree, env)

            def k(a):
                return run(f.force()(a), cofree, env).force()

            return suspend(ma.bind, delay(k))

        # ----- Comonad ---------------------------------------------------------
        # Core Comonad operations. `extend` is derived and lowered through
        # `duplicate` and `fmap`, so only extract and duplicate are primitive.

        case Extract(wa):
            wa = run(wa.force(), cofree, env).force()
            return suspend(wa.extract)

        case Duplicate(wa):
            wa = run(wa.force(), cofree, env).force()
            return suspend(wa.duplicate)

        # ----- Semigroupoid -----------------------------------------------------
        # Sequential composition of morphisms.

        case Compose(fbc, fab):
            fbc = run(fbc.force(), cofree, env).force()
            fab = run(fab.force(), cofree, env)

            return suspend(fbc.compose, fab)

        # ----- Category ---------------------------------------------------------
        # Identity morphism.

        case ID(cls):
            return suspend(cls.id)

        # ----- Groupoid ---------------------------------------------------------
        # Identity morphism.

        case Invert(fab):
            fab = run(fab.force(), cofree, env).force()
            return suspend(fab.invert)

        # ----- Semigroup --------------------------------------------------------
        # Binary associative combination.

        case Combine(a, b):
            a = run(a.force(), cofree, env).force()
            b = run(b.force(), cofree, env)

            return suspend(a.combine, b)

        # ----- Monoid -----------------------------------------------------------
        # Identity element for a Semigroup.

        case MEmpty(cls):
            return suspend(cls.mempty)

        # ----- Group ------------------------------------------------------------
        # Inversion operation for Group structures.

        case Inverse(fab):
            fab = run(fab.force(), cofree, env).force()

            return suspend(fab.inverse)

        # ----- Arrow ------------------------------------------------------------
        # Core Arrow operations and derived combinators expressed in terms of
        # arr and first. Derived operations are lowered into simpler Arrow
        # expressions and reruned.

        case Arr(cls, fab):
            def k(a):
                return run(fab.force(), cofree, env).force()(a)
            return suspend(cls.arrow, delay(k))

        case First(cls, aab):
            def k(a):
                return run(aab.force(), cofree, env).force()(a)
            return suspend(cls.first, delay(k))

        case Second(cls, aab):
            def swap(pair):
                x, y = pair
                return (y, x)

            arrswap = delay(Arr(cls, delay(swap)))
            first   = delay(First(cls, aab))

            one  = delay(Compose(first, arrswap))
            comp = Compose(arrswap, one)

            return resume(run, comp, cofree, env)

        case Split(cls, aab, acd):
            first_  = delay(First(cls, aab))
            second_ = delay(Second(cls, acd))

            comp = Compose(second_, first_)
            return resume(run, comp, cofree, env)

        case Fanout(cls, aab, aac):
            def duplicate(a):
                return (a, a)
            
            arrduplicate = delay(Arr(cls, delay(duplicate)))
            split = delay(Split(cls, aab, aac))
            comp = Compose(split, arrduplicate)

            return resume(run, comp, cofree, env)

        # ----- ArrowChoice  -----------------------------------------------------
        # Core Arrow operations and derived combinators expressed in terms of
        # arr and first. Derived operations are lowered into simpler Arrow
        # expressions and reruned.

        case Left(cls, aab):
            def k(a):
                return run(aab.force(), cofree, env).force()(a)
            return suspend(cls.left, delay(k))

        case Right(cls, aab):
            def swap(e):
                match e:
                    case ELeft(x):
                        return ERight(x)
                    case ERight(x):
                        return ELeft(x)

            arrswap = delay(Arr(cls, delay(swap)))
            left_   = delay(Left(cls, aab))

            one  = delay(Compose(left_, arrswap))
            comp = Compose(arrswap, one)

            return resume(run, comp, cofree, env)

        case PlusPlus(cls, aab, acd):
            left_  = delay(Left(cls, aab))
            right_ = delay(Right(cls, acd))
            comp   = Compose(right_, left_)
            return resume(run, comp, cofree, env)

        case OrOr(cls, aab, acb):
            def merge(e):
                match e:
                    case ELeft(b):
                        return b
                    case ERight(b):
                        return b

            ppg = delay(PlusPlus(cls, aab, acb))
            arrmerge = delay(Arr(cls, delay(merge)))

            comp = Compose(arrmerge, ppg)
            return resume(run, comp, cofree, env)

        # ----- ArrowApply  -----------------------------------------------------
        # Dynamic arrow application. Allows an arrow produced at runtime to be
        # immediately applied.

        case Apply(cls):
            return resume(run, cls.app(), cofree, env)

        # ----- Base ------------------------------------------------------------
        # Base case: already a runtime value.

        case _:
            return Thunk(lambda: free)

## from typeclass.typeclasses.functor.interpret import HANDLERS as FUNCTOR
## from typeclass.typeclasses.applicative.interpret import HANDLERS as APPLICATIVE
## from typeclass.typeclasses.alternative.interpret import HANDLERS as ALTERNATIVE
## from typeclass.typeclasses.monad.interpret import HANDLERS as MONAD
## from typeclass.typeclasses.comonad.interpret import HANDLERS as COMONAD
## from typeclass.typeclasses.semigroupoid.interpret import HANDLERS as SEMIGROUPOID
## from typeclass.typeclasses.category.interpret import HANDLERS as CATEGORY
## from typeclass.typeclasses.groupoid.interpret import HANDLERS as GROUPOID
## from typeclass.typeclasses.semigroup.interpret import HANDLERS as SEMIGROUP
## from typeclass.typeclasses.monoid.interpret import HANDLERS as MONOID
## from typeclass.typeclasses.group.interpret import HANDLERS as GROUP
## from typeclass.typeclasses.arrow.interpret import HANDLERS as ARROW
## from typeclass.typeclasses.arrowchoice.interpret import HANDLERS as ARROWCHOICE
## from typeclass.typeclasses.arrowapply.interpret import HANDLERS as ARROWAPPLY
## 
## HANDLERS = {}
## for group in (
##     FUNCTOR,
##     APPLICATIVE,
##     ALTERNATIVE,
##     MONAD,
##     COMONAD,
##     SEMIGROUPOID,
##     CATEGORY,
##     GROUPOID,
##     SEMIGROUP,
##     MONOID,
##     GROUP,
##     ARROW,
##     ARROWCHOICE,
##     ARROWAPPLY,
## ):
##     HANDLERS.update(group)
## 
## def run(expr, cofree=None, env=None):
##     handler = HANDLERS.get(type(expr))
##     if handler is None:
##         return expr
##     return handler(expr, run, cofree, env)
