if __name__ == "__main__":
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.thunk import Thunk
    from typeclass.syntax.symbols import pure, fmap, ap, otherwise
    from typeclass.interpret.interpreter import interpret
