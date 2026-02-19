if __name__ == "__main__":
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.thunk import Thunk
    from typeclass.syntax.symbols import fmap, pure, ap, then, skip, empty, otherwise, some, many
    from typeclass.interpret.interpreter import interpret

    free = Just(10) |fmap| (lambda x: x + 5)
    result = interpret(free, None, None).force()
    print(result, result == Just(15))

    free = Just |pure| (lambda x: lambda y: x + y) |ap| Just(10) |ap| Just(11)
    result = interpret(free, None, None).force()
    print(result, result == Just(21))

    free = many(Thunk(lambda: empty(Maybe)), Maybe)
    result = interpret(free, None, None).force()
    print(result, result == Just([]))

    from typeclass.data.thunk import Thunk
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.syntax.alternative import some, many, otherwise, empty
    from typeclass.syntax.applicative import pure, liftA2
    from typeclass.interpret.interpreter import interpret
    
    # v = empty Maybe (aka failure)
    v = Thunk(lambda: empty(Maybe))
    
    expr_some = some(v, Maybe)   # should be empty
    expr_many = many(v, Maybe)   # should be Just([])
    
    print("some(empty) =", interpret(expr_some, None, None).force())
    print("many(empty) =", interpret(expr_many, None, None).force())
    
    # Now build something slightly richer:
    # many(empty) gives Just([])
    # liftA2 can combine two applicatives; this becomes Just(len([]) + 10) = Just(10)
    expr = liftA2(lambda xs, n: len(xs) + n, expr_many, pure(Maybe, 10))
    print("liftA2(len(many(empty)) + 10) =", interpret(expr, None, None).force())
    
    # Alternative fallback: empty <|> pure(99)  => Just(99)
    expr_alt = otherwise(empty(Maybe), pure(Maybe, 99))
    print("empty <|> pure(99) =", interpret(expr_alt, None, None).force())


