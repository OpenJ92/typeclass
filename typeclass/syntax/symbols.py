from typeclass.syntax.infix import Infix
from typeclass.protocols.functor import fmap, replace
from typeclass.protocols.applicative import ap, pure, then, skip
from typeclass.protocols.alternative import otherwise, empty

fmap    = Infix(fmap)
replace = Infix(replace)
ap   = Infix(ap)
pure = Infix(pure)
then = Infix(then)
skip = Infix(skip)
otherwise = Infix(otherwise)
empty = Infix(empty)
