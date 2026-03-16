from typeclass.typeclasses.infix import Infix
from typeclass.typeclasses.functor import fmap, replace, void
from typeclass.typeclasses.applicative import ap, pure, then, skip, liftA2
from typeclass.typeclasses.alternative import otherwise, empty, some, many
from typeclass.typeclasses.monad import bind, return_, mthen, join, rbind, kleisli, rkleisli
from typeclass.typeclasses.comonad import extract, duplicate, extend
from typeclass.typeclasses.semigroupoid import compose, rcompose
from typeclass.typeclasses.category import identity
from typeclass.typeclasses.groupoid import invert
from typeclass.typeclasses.semigroup import combine
from typeclass.typeclasses.monoid import mempty
from typeclass.typeclasses.group import inverse
from typeclass.typeclasses.arrow import arrow, first, second, split, fanout
from typeclass.typeclasses.arrowchoice import left, right, plusplus, oror
from typeclass.typeclasses.arrowapply import apply

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
extend = Infix(extend)
