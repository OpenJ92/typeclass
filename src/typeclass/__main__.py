if __name__ == "__main__":
    from typeclass.data.thunk import Thunk
    from typeclass.data.maybe import Maybe, Just, Nothing
    from typeclass.data.parser import Parser, item, satisfy, char, one_of, none_of
    from typeclass.data.reader import Reader
    from typeclass.data.morphism import Morphism as M
    from typeclass.data.endomorphism import Endomorphism as E
    from typeclass.data.isomorphism import Isomorphism
    from typeclass.data.automorphism import Automorphism
    from typeclass.data.either import Left, Right
    from typeclass.data.sequence import Sequence, concat, from_iterable, zipwith
    from typeclass.data.tree import Tree, pretty, embed
    from typeclass.data.streamtree import StreamTree, realize, depths, widths, paths, coordinates
    from typeclass.typeclasses.applicative import pure, liftA2
    from typeclass.typeclasses.symbols import fmap, pure, ap, then, skip, empty, otherwise, some, many, return_, bind, \
    compose, rcompose, identity, invert, combine, mempty, inverse, arrow, first, second, split, fanout, \
    left, right, plusplus, oror, apply, duplicate, extract
    from typeclass.interpret.run import run
