from typeclass.syntax.infix import Infix
from typeclass.protocols.functor import fmap, replace
from typeclass.protocols.applicative import ap, pure, then, skip

fmap    = Infix(fmap)
replace = Infix(replace)
ap   = Infix(ap)
pure = Infix(pure)
then = Infix(then)
skip = Infix(skip)
