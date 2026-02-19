from typeclass.syntax.functor import Map
from typeclass.syntax.applicative import Ap, Pure
from typeclass.syntax.alternative import Otherwise, Empty, Some, Many

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
        
        case Many(v, internal):
            some = Thunk(lambda: Some(v, internal))
            pure = Thunk(lambda: Pure(internal, Thunk(lambda: [])))
            otherwise = Otherwise(some, pure)
            return Thunk(lambda: interpret(otherwise, None, None).force())

        case Some(v, internal):
            cons = (lambda x: (lambda xs: [x] + xs))
            map  = Thunk(lambda: Map(cons, v))
            many = Thunk(lambda: Many(v, internal))
            ap   = Ap(map, many)
            return Thunk(lambda: interpret(ap, None, None).force())

        case _:
            return Thunk(lambda: free)


