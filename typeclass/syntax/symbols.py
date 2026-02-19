from typeclass.syntax.infix import Infix
from typeclass.syntax.functor import fmap, replace
from typeclass.syntax.applicative import ap, pure, then, skip
from typeclass.syntax.alternative import otherwise, empty, some, many

fmap    = Infix(fmap)
replace = Infix(replace)
ap   = Infix(ap)
pure = Infix(pure)
then = Infix(then)
skip = Infix(skip)
otherwise = Infix(otherwise)
