from typeclass.syntax.functor import FreeMap
from typeclass.syntax.applicative import FreeAp, FreePure
from typeclass.data.thunk import Thunk

def interpret(free_expr, cofree, env):

    match free_expr:
        case FreePure(cls, value):
            return Thunk(lambda: cls.pure(value.force()))

        case FreeMap(function, value):
            return Thunk(lambda: value.force().fmap(function))

        case FreeAp(free_func, free_arg):
            def defered():
                f = interpret(free_func.force(), None, None).force()
                if f == type(f).empty():
                    return Thunk(lambda: type(f).empty())

                x = interpret(free_arg.force(), None, None).force()
                if x == type(x).empty():
                    return Thunk(lambda: type(x).empty())

                return f.ap(x)
            return Thunk(defered)
        case _:
            return Thunk(lambda: free_expr)


