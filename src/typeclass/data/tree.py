from dataclasses import dataclass
from typing import Generic, TypeVar

from typeclass.data.thunk import Thunk
from typeclass.data.sequence import Sequence, Cons, Nil
from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative

A = TypeVar("A")

@dataclass(frozen=True)
class Tree(Applicative[A], Functor[A], Generic[A]):
    value: A
    children: Seq[Tree[A]]

    # ----- Functor ---------------------------------------------------------

    def fmap(self: Tree[A], f: Callable[[A], B]) -> Tree[B]:
        match self:
            case Tree(value=value, children=children):
                nf = f.force()
                nchildren = children.fmap(lambda tree: tree.fmap(f))
                return Tree(nf(value), nchildren)

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> Tree[A]:
        return Tree(value, Sequence.empty())

    def ap(self: Tree[Callable[[A], B]], fa: Tree[A]) -> Tree[B]:
        _fa = fa.force()

        def zip_ap( fs: Sequence[Tree[Callable[[A], B]]], xs: Sequence[Tree[A]],) -> Seq[Tree[B]]:
            match (fs, xs):
                case (Cons(head=fh, tail=ft), Cons(head=xh, tail=xt)):
                    return Cons(fh.ap(Thunk(lambda: xh)), zip_ap(ft, xt))
                case _:
                    return Nil()

        match (self, _fa):
            case (Tree(value=f, children=fs), Tree(value=a, children=xs)):
                return Tree(f(a), zip_ap(fs, xs))
