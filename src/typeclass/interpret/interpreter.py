from typeclass.syntax.functor import Map from typeclass.syntax.applicative import Ap, Pure
from typeclass.syntax.alternative import Otherwise, Empty, Some, Many
from typeclass.syntax.monad import Bind, Return

from typeclass.data.thunk import Thunk

def interpret(free, cofree, env):

    match free:

        case Map(function, value):
            value = interpret(value.force(), None, None).force()
            return Thunk(lambda: value.fmap(function))

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
        
        case Many(internal, v):
            some = Thunk(lambda: Some(internal, v))
            pure = Thunk(lambda: Pure(internal, Thunk(lambda: [])))
            otherwise = Otherwise(some, pure)
            return Thunk(lambda: interpret(otherwise, None, None).force())

        case Some(internal, v):
            cons = (lambda x: (lambda xs: [x] + xs))
            map  = Thunk(lambda: Map(cons, v))
            many = Thunk(lambda: Many(internal, v))
            ap   = Ap(map, many)
            return Thunk(lambda: interpret(ap, None, None).force())

        case Return(cls, value):
            value = interpret(value.force(), None, None).force()
            return Thunk(lambda: cls.pure(value))

        case Bind(ma, f):
            ma = interpret(ma.force(), None, None).force()
            f = interpret(f.force(), None, None))

            def k(a):
                return interpret(f.force()(a), None, None)

            return Thunk(lambda: ma.bind(Thunk(lambda: k)))

        case _:
            return Thunk(lambda: free)


