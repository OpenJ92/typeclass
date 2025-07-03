from typeclass.syntax.functor import Map
from typeclass.syntax.applicative import Ap, Pure
from typeclass.syntax.alternative import Otherwise, Empty

from typeclass.data.thunk import Thunk

def interpret(free, cofree, env):

    match free:

        case Map(function, value):
            return Thunk(lambda: value.force().fmap(function))

        case Pure(cls, value):
            return Thunk(lambda: cls.pure(value.force()))

        case Ap(function, value):
            function = interpret(function.force(), None, None).force()
            if function == type(function).empty():
                return Thunk(lambda: type(function).empty())

            value = interpret(value.force(), None, None).force()
            if value == type(value).empty():
                return Thunk(lambda: type(value).empty())

            return Thunk(lambda: function.ap(value))

        case Empty(cls):
            return Thunk(lambda: cls.empty())

        case Otherwise(alter, native):
            alter = interpret(alter.force(), None, None).force()
            if alter != type(alter).empty():
                return Thunk(lambda: alter)

            native = interpret(native.force(), None, None).force()
            if native != type(native).empty():
                return Thunk(lambda: native)

            return Thunk(lambda: alter.otherwise(native))

        case _:
            return Thunk(lambda: free)


