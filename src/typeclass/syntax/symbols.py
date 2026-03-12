from typeclass.syntax.infix import Infix
from typeclass.syntax.functor import fmap, replace, void
from typeclass.syntax.applicative import ap, pure, then, skip, liftA2
from typeclass.syntax.alternative import otherwise, empty, some, many
from typeclass.syntax.monad import bind, return_, mthen, join, rbind, kleisli, rkleisli
from typeclass.syntax.semigroupoid import compose, rcompose
from typeclass.syntax.category import identity
from typeclass.syntax.groupoid import invert
from typeclass.syntax.semigroup import combine
from typeclass.syntax.monoid import mempty
from typeclass.syntax.group import inverse
from typeclass.syntax.arrow import arrow, first, second, split, fanout
from typeclass.syntax.arrowchoice import left, right, plusplus, oror
from typeclass.syntax.arrowapply import apply

fmap    = Infix(fmap)
replace = Infix(replace)
ap   = Infix(ap)
pure = Infix(pure)
then = Infix(then)
skip = Infix(skip)
otherwise = Infix(otherwise)
some = Infix(some)
many = Infix(many)
bind = Infix(bind)
return_ = Infix(return_)
mthen = Infix(mthen)
rbind = Infix(rbind)
kleisli = Infix(kleisli)
rkleisli = Infix(rkleisli)
compose = Infix(compose)
rcompose = Infix(rcompose)
combine = Infix(combine)
arrow = Infix(arrow)
first = Infix(first)
second = Infix(second)
split = Infix(split)
fanout = Infix(fanout)
left = Infix(left)
right = Infix(right)
plusplus = Infix(plusplus)
oror = Infix(oror)
