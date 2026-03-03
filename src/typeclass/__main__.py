if __name__ == "__main__":
    from typeclass.data.thunk import Thunk
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.parser import Parser
    from typeclass.data.reader import Reader
    from typeclass.data.morphism import Morphism
    from typeclass.data.endomorphism import Endomorphism
    from typeclass.data.isomorphism import Isomorphism
    from typeclass.data.automorphism import Automorphism
    from typeclass.syntax.applicative import pure, liftA2
    from typeclass.syntax.symbols import fmap, pure, ap, then, skip, empty, otherwise, some, many, return_, bind, \
    compose, rcompose, identity, invert, combine, mempty, inverse
    from typeclass.interpret.interpreter import interpret

    free = Just(10) |fmap| (lambda x: x + 5)
    result = interpret(free, None, None).force()
    print(result, result == Just(15))

    free = Just |pure| (lambda x: lambda y: x + y) |ap| Just(10) |ap| Just(11)
    result = interpret(free, None, None).force()
    print(result, result == Just(21))

    free = Maybe |many| Thunk(lambda: empty(Maybe))
    result = interpret(free, None, None).force()
    print(result, result == Just([]))

    # v = empty Maybe (aka failure)
    v = Thunk(lambda: empty(Maybe))
    
    expr_some = Maybe |some| v  # should be empty
    expr_many = Maybe |many| v  # should be Just([])
    
    print("some(empty) =", interpret(expr_some, None, None).force())
    print("many(empty) =", interpret(expr_many, None, None).force())
    
    # Now build something slightly richer:
    # many(empty) gives Just([])
    # liftA2 can combine two applicatives; this becomes Just(len([]) + 10) = Just(10)
    expr = liftA2(lambda xs, n: len(xs) + n, expr_many, Maybe |pure| 10)
    print("liftA2(len(many(empty)) + 10) =", interpret(expr, None, None).force())
    
    # Alternative fallback: empty <|> pure(99)  => Just(99)
    expr_alt = empty(Maybe) |otherwise| (Maybe |pure| 99)
    print("empty <|> pure(99) =", interpret(expr_alt, None, None).force())


    ## Parser Example
    def digit() -> Parser[str]:
        def run(s: str):
            if s and s[0].isdigit():
                return [(s[0], s[1:])]
            return []
        return Parser(run)

    def _combine(a):
        return lambda b: int(a + b)

    def char(a):
        def run(s: str):
            if s and s[0] == a:
                return [(s[0], s[1:])]
            return []
        return Parser(run)

    free = Parser |pure| _combine |ap| digit() |ap| digit()
    result = interpret(free, None, None).force().run("42xyz")
    print(result, result == [(42, "xyz")])

    digits = Parser |many| digit()
    result = interpret(digits, None, None).force().run("42xyz")
    print(result, result == [(['4', '2'], "xyz")])

    whitespace = Parser |many| (char(" ") |otherwise| char("\t"))
    result = interpret(whitespace, None, None).force().run(" \t42xyz")
    print(result, result == [([' ', '\t'], '42xyz')])

    number = Parser |some| digit() |fmap| (lambda xs: int("".join(xs)))
    result = interpret(number, None, None).force().run("271828xyz")
    print(result, result == [(271828, 'xyz')])

    def plus_one(x: int):
        return Just(x+1)

    free = Maybe |pure| 10 |bind| plus_one
    result = interpret(free, None, None).force()
    print(result, result == Just(11))

    free = digit() |bind| (lambda d: char(str(int(d) + 1)))
    result = interpret(free, None, None).force().run("343")
    print(result, result == [('4', '3')])

    free = Parser |many| free
    result = interpret(free, None, None).force().run("123456789")
    print(result, result == [(['2', '4', '6', '8'], '9')])

    free = Reader(lambda x: 10*x) |fmap| (lambda y: 5*str(y))
    result = interpret(free, None, None).force().run(1)
    print(result, result == "1010101010")

    free = Reader(lambda x: x + 1) |bind| (lambda y: Reader(lambda x: x + y))
    result = interpret(free, None, None).force().run(10)
    print(result, result == 21)

    free = Reader |pure| (lambda x: lambda y: (x, y)) \
                    |ap|    Reader(lambda x: x)       \
                    |ap|    Reader(lambda y: 2*y)
    result = interpret(free, None, None).force().run(10)
    print(result, result == (10,20))

    free = Morphism(lambda x: x + 1) |compose| Morphism(lambda y: y * y)
    result = interpret(free, None, None).force()(10)
    print(result, result == 101)

    free = Morphism(lambda x: x * x) |rcompose| Morphism(lambda y: y + 1)
    result = interpret(free, None, None).force()(10)
    print(result, result == 101)

    function = lambda x: x + 1
    forward  = identity(Morphism) |compose| Morphism(function)
    backward = Morphism(function) |compose| identity(Morphism)
    fresult = interpret(forward, None, None).force()(10)
    bresult = interpret(backward, None, None).force()(10)
    print(f"{fresult} == {bresult}", fresult == bresult)

    function = lambda x: lambda y: x + y
    left  = (Morphism(function(1)) |compose| Morphism(function(2))) |compose| Morphism(function(3))
    right = Morphism(function(1)) |compose| (Morphism(function(2)) |compose| Morphism(function(3)))
    lresult = interpret(left, None, None).force()(10)
    rresult = interpret(right, None, None).force()(10)
    print(f"{lresult} == {rresult}", lresult == rresult)

    from math import sqrt
    auto = Isomorphism(lambda x: x*x, sqrt)
    free = invert(auto)
    free = auto |compose| free
    result = interpret(free, None, None).force()
    print(result(0), result(0) == 0)

    left = lambda x: x + 1
    right = lambda x: x - 1
    endo = Endomorphism(left) |combine| Endomorphism(right)
    result = interpret(endo, None, None).force()
    print(result(0), result(0) == 0)

    endo = Endomorphism(left)
    identity = mempty(Endomorphism)
    forward = endo |combine| identity
    backward = identity |combine| endo

    fresult = interpret(forward, None, None).force()
    bresult = interpret(backward, None, None).force()

    print(f"{fresult(10)} == {bresult(10)}", fresult(10) == bresult(10))

    from math import cos, acos, pi
    auto = Automorphism(cos, acos)
    ainv = inverse(auto)
    back = ainv |combine| auto
    bresult = interpret(back, None, None).force()

    print(bresult(pi), bresult(pi) == pi)


