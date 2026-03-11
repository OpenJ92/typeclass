if __name__ == "__main__":
    from typeclass.data.thunk import Thunk
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.parser import Parser
    from typeclass.data.reader import Reader
    from typeclass.data.morphism import Morphism as M
    from typeclass.data.endomorphism import Endomorphism as E
    from typeclass.data.isomorphism import Isomorphism
    from typeclass.data.automorphism import Automorphism
    from typeclass.data.either import Left, Right
    from typeclass.data.sequence import Sequence, Cons, Nil
    from typeclass.data.tree import Tree
    from typeclass.syntax.applicative import pure, liftA2
    from typeclass.syntax.symbols import fmap, pure, ap, then, skip, empty, otherwise, some, many, return_, bind, \
    compose, rcompose, identity, invert, combine, mempty, inverse, arrow, first, second, split, fanout, \
    left, right, plusplus, oror, apply
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

    free = M(lambda x: x + 1) |compose| M(lambda y: y * y)
    result = interpret(free, None, None).force()(10)
    print(result, result == 101)

    free = M(lambda x: x * x) |rcompose| M(lambda y: y + 1)
    result = interpret(free, None, None).force()(10)
    print(result, result == 101)

    function = lambda x: x + 1
    forward  = identity(M) |compose| M(function)
    backward = M(function) |compose| identity(M)
    fresult = interpret(forward, None, None).force()(10)
    bresult = interpret(backward, None, None).force()(10)
    print(f"{fresult} == {bresult}", fresult == bresult)

    function = lambda x: lambda y: x + y
    _left  = (M(function(1)) |compose| M(function(2))) |compose| M(function(3))
    _right = M(function(1)) |compose| (M(function(2)) |compose| M(function(3)))
    lresult = interpret(_left, None, None).force()(10)
    rresult = interpret(_right, None, None).force()(10)
    print(f"{lresult} == {rresult}", lresult == rresult)

    from math import sqrt
    auto = Isomorphism(lambda x: x*x, sqrt)
    free = invert(auto)
    free = auto |compose| free
    result = interpret(free, None, None).force()
    print(result(0), result(0) == 0)

    _left = lambda x: x + 1
    _right = lambda x: x - 1
    endo = E(_left) |combine| E(_right)
    result = interpret(endo, None, None).force()
    print(result(0), result(0) == 0)

    endo = E(_left)
    identity = mempty(E)
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

    free = (endo |split| (E, endo)) |compose| (endo |fanout| (E, endo))
    result = interpret(free, None, None).force()
    print(f"{result(10)} == (12,12)", result(10) == (12,12))

    def add(pair):
        pair, x = pair
        if isinstance(pair, int):
            return pair + x
        return x + add(pair)

    def flatten(pair):
        pair, x = pair
        if isinstance(pair, tuple):
            return (*flatten(pair), x)
        return (pair, x)

    free = (M |arrow| flatten)                                      \
         |compose| (endo |split| (E, endo) |split| (E, E(_right))) \
         |compose| (endo |fanout| (E, endo) |fanout| (E, endo))
    result_ = interpret(free, None, None).force()
    print(f"{result_(10)} == ((12,12), 10)", result_(10) == (12,12,10))

    deep = M |arrow| flatten \
         |compose| (endo |split|  (E, endo) |split|  (E, endo) |split|  (E, endo)) \
         |compose| (endo |split|  (E, endo) |split|  (E, endo) |split|  (E, endo)) \
         |compose| (endo |split|  (E, endo) |split|  (E, endo) |split|  (E, endo)) \
         |compose| (endo |fanout| (E, endo) |fanout| (E, endo) |fanout| (E, endo))              
    result = interpret(deep, None, None).force()

    inc = M(lambda x: x + 1)

    free = E |second| inc
    result = interpret(free, None, None).force()((10, 20))
    print(result, result == (10, 21))

    # second composed with first
    free = (E |first| inc) |compose| free
    result = interpret(free, None, None).force()((10, 20))
    # first:  (10,20) -> (11,20)
    # second: (11,20) -> (11,21)
    print(result, result == (11, 21))

    inc = M(lambda x: x + 1)

    free = M |left| inc
    run = interpret(free, None, None).force()
    print(run(Left(10)),  run(Left(10))  == Left(11))
    print(run(Right("x")), run(Right("x")) == Right("x"))

    free = M |right| inc
    run = interpret(free, None, None).force()
    print(run(Left("x")),  run(Left("x"))  == Left("x"))
    print(run(Right(10)),  run(Right(10))  == Right(11))

        # --- ArrowChoice +++ example ---
    inc = M(lambda x: x + 1)
    dbl = M(lambda x: 2 * x)

    free = inc |plusplus| (M, dbl)
    run = interpret(free, None, None).force()

    print(run(Left(10)),   run(Left(10))   == Left(11))   # Left branch uses inc
    print(run(Right(10)),  run(Right(10))  == Right(20))  # Right branch uses dbl

        # --- ArrowChoice ||| (oror) example ---
    inc = M(lambda x: x + 1)
    dbl = M(lambda x: 2 * x)

    free = inc |oror| (M, dbl)
    run = interpret(free, None, None).force()

    print(run(Left(10)),   run(Left(10))   == 11)  # Left branch returns B
    print(run(Right(10)),  run(Right(10))  == 20)  # Right branch returns B

        # --- Stop-or-continue shape: Either drives branching ---
    # Left means "done", Right means "continue"; oror chooses.
    done = M(lambda x: x)            # B -> B
    cont = M(lambda x: x + 1000)     # A -> B (just to show different path)

    free = done |oror| (M, cont)
    run = interpret(free, None, None).force()
    print(run(Left(7)),   run(Left(7))   == 7)
    print(run(Right(7)),  run(Right(7))  == 1007)

    inc    = M(lambda x: x + 1)
    times3 = M(lambda x: x * 3)
    sq     = M(lambda x: x * x)
    strlen = M(lambda s: len(s))
    
    # Left branch:  int -> (x+1) -> (*3)
    left_prog  =  times3 |compose| inc
    
    # Right branch: str -> len -> square
    right_prog = sq |compose| strlen 
    
    # Route: Either[int, str] -> Either[int, int]
    routed = left_prog |plusplus| (M, right_prog)

    run_routed = interpret(routed, None, None).force()
    print("routed Left:", run_routed(Left(10)))
    print("routed Right:", run_routed(Right("hi")))
    
    # Collapse: Either[int, int] -> int via oror (id ||| id)
    id_int = M(lambda x: x)
    free = (id_int |oror| (M, id_int)) |compose| routed  
    
    run = interpret(free, None, None).force()
    
    print(run(Left(10)), run(Left(10)) == 33)          # (10+1)*3 = 33
    print(run(Right("hi")), run(Right("hi")) == 4)     # len=2, sq=4
    print(run(Right("abcd")), run(Right("abcd")) == 16)

    inc   = M(lambda x: x + 1)
    dbl   = M(lambda x: 2 * x)
    upper = M(lambda s: s.upper())
    
    tagL  = M(lambda n: f"L:{n}")
    tagRL = M(lambda s: f"RL:{s}")
    tagRR = M(lambda n: f"RR:{n}")
    
    # inner : Either[str, int] -> str
    inner = (upper |rcompose| tagRL) |oror| (M, (dbl |rcompose| tagRR))
    
    # whole : Either[int, Either[str, int]] -> str
    free = (inc |rcompose| tagL) |oror| (M, inner)

    run = interpret(free, None, None).force()
    
    print(run(Left(10)),             run(Left(10))             == "L:11")
    print(run(Right(Left("hi"))),    run(Right(Left("hi")))    == "RL:HI")
    print(run(Right(Right(7))),      run(Right(Right(7)))      == "RR:14")

        # --- Stop-or-continue with self-reference on the Right branch ---
    # Left means done. Right means continue by feeding back into the same graph.

    done = M(lambda x: x + 100)   # easy-to-see terminal action
    free = done |plusplus| (M, free)

    run = interpret(free, None, None).force()

    print("gated recursive Left:", run(Left(7)), run(Left(7)) == Left(107))

    # This is the recursive path.
    # It should keep re-entering the same expression if knot-tying worked.
    # print("gated recursive Right:", run(Right(7)))
    step = M(lambda n: Left(n) if n <= 0 else Right(n - 1))
    done = M(lambda n: n + 100)
    
    base = step |oror| (M, M(lambda n: n))
    
    run_base = interpret(base, None, None).force()
    print(run_base(Left(10)))    # 0
    print(run_base(Right(30)))   # 3

    def from_iterable(iterable):
        """
        Construct a Sequence from any iterable.

        Elements are inserted in the same order as the iterable.
        """
        result = Nil()
        for x in reversed(list(iterable)):
            result = Cons(x, result)
        return result

    l = from_iterable([1, 2, 3, 4, 5, 6])

