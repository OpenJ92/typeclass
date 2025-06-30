if __name__ == "__main__":
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.thunk import Thunk
    from typeclass.syntax.symbols import pure, fmap, ap, otherwise

    # Constructing Just and Nothing
    a = Just(10)
    b = Nothing()

    print("a:", a)                    # Just(10)
    print("b:", b)                    # Nothing()

    # fmap usage
    inc = lambda x: x + 1
    print("fmap inc over a:", a |fmap| inc)   # Just(11)
    print("fmap inc over b:", b |fmap| inc)   # Nothing()

    # ap usage
    plus = lambda x: lambda y: x + y
    add_fn = Just(plus(3))            # Just(lambda y: 3 + y)
    val = Just(4)

    print("ap: Just(3+) <*> Just(4):", add_fn |ap| (lambda: val))    # Just(7)
    print("ap: Nothing <*> Just(4):", b |ap| (lambda: val))          # Nothing()

    # otherwise usage
    print("a |otherwise| b:", a |otherwise| b)             # Just(10)
    print("b |otherwise| a:", b |otherwise| a)             # Just(10)

    # empty usage
    print("empty(Maybe) |otherwise| a:", Maybe.empty() |otherwise| a)  # Just(10)

    # pure usage
    print("pure(Maybe, 42):", Maybe |pure| 42)             # Just(42)

    # some/many usage (greedy repetition)
    from typeclass.data.thunk import some, many

    counter = 3

    def parser() -> Thunk:
        global counter
        print("[parser] Counter:", counter)
        if counter <= 0:
            return Nothing()
        counter -= 1
        return Just("There")

    # Thunk-wrapped parser

    # Use `many` with explicit internal type `Just`
    result = many(Thunk(parser), Maybe)
    print(result.force())


