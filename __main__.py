if __name__ == "__main__":
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.thunk import Thunk
    from typeclass.syntax.symbols import fmap, pure, ap, then, skip, empty, otherwise, some, many
    from typeclass.interpret.interpreter import interpret

    counter = {"n": 7}  # or any number you want to test

    def decrementing_parser():
        if counter["n"] <= 0:
            print("→ Nothing")
            return Nothing()
        else:
            print(f"→ Just({counter['n']})")
            value = counter["n"]
            counter["n"] -= 1
            return Just(value)
