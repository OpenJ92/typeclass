from typeclass.syntax.value import Value
from typeclass.syntax.functor import Map 
from typeclass.syntax.applicative import Ap, Pure
from typeclass.syntax.alternative import Otherwise, Empty, Some, Many
from typeclass.syntax.monad import Bind, Return
from typeclass.syntax.semigroupoid import Compose
from typeclass.syntax.category import ID
from typeclass.syntax.groupoid import Invert
from typeclass.syntax.semigroup import Combine
from typeclass.syntax.monoid import MEmpty
from typeclass.syntax.group import Inverse
from typeclass.syntax.arrow import Arr, First, Split, Fanout

from typeclass.data.thunk import Thunk

def interpret(free, cofree, env):

    match free:

        case Map(function, value):
            value = interpret(value.force(), None, None).force()
            function = interpret(function.force(), None, None)

            def k(a):
                return interpret(function.force()(a), None, None).force()

            return Thunk(lambda: value.fmap(Thunk(lambda: k)))

        case Pure(cls, value):
            value = interpret(value.force(), None, None).force()
            return Thunk(lambda: cls.pure(value))

        case Ap(function, value):
            function = interpret(function.force(), None, None).force()
            value    = interpret(value.force(), None, None)
            return Thunk(lambda: function.ap(value))

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

        case Return(cls, value):
            value = interpret(value.force(), None, None).force()
            return Thunk(lambda: cls.pure(value))

        case Bind(ma, f):
            ma = interpret(ma.force(), None, None).force()
            f = interpret(f.force(), None, None)

            def k(a):
                return interpret(f.force()(a), None, None).force()

            return Thunk(lambda: ma.bind(Thunk(lambda: k)))

        case Compose(fbc, fab):
            fbc = interpret(fbc.force(), None, None).force()
            fab = interpret(fab.force(), None, None)

            return Thunk(lambda: fbc.compose(fab))

        case ID(cls):
            return Thunk(lambda: cls.id())

        case Invert(fab):
            fab = interpret(fab.force(), None, None).force()
            return Thunk(lambda: fab.invert())

        case Combine(a, b):
            a = interpret(a.force(), None, None).force()
            b = interpret(b.force(), None, None)

            return Thunk(lambda: a.combine(b))

        case MEmpty(cls):
            return Thunk(lambda: cls.mempty())

        case Inverse(fab):
            fab = interpret(fab.force(), None, None).force()

            return Thunk(lambda: fab.inverse())

        case Arr(cls, fab):
            return Thunk(lambda: cls.arrow(fab))

        case First(aab):
            aab = interpret(aab.force(), None, None).force()
            return Thunk(lambda: aab.first())

        case Split(aab, acd):
            def swap(pair):
                x, y = pair
                return (y, x)

            aab = interpret(aab.force(), None, None).force()

            arrswap = Thunk(lambda: Arr(type(aab), Thunk(lambda: swap)))
            faab = Thunk(lambda: First(Thunk(lambda: Value(aab))))
            facd = Thunk(lambda: First(acd))
            one = Thunk(lambda: Compose(faab, arrswap))
            two = Thunk(lambda: Compose(one, facd))
            comp = Compose(two, arrswap)

            return Thunk(lambda: interpret(comp, None, None).force())

        case Fanout(aab, aac):
            def duplicate(a):
                return (a, a)
            
            aab = interpret(aab.force(), None, None).force()

            arrduplicate = Thunk(lambda: Arr(type(aab), Thunk(lambda: duplicate)))
            split = Thunk(lambda: Split(Thunk(lambda: Value(aab)), aac))
            comp = Compose(split, arrduplicate)

            return Thunk(lambda: interpret(comp, None, None).force())

        case Value(value):
            return Thunk(lambda: value)
        case _:
            return Thunk(lambda: free)


