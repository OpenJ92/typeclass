from dataclasses import dataclass
from typing import Generic, TypeVar, Callable

from typeclass.data.thunk import Thunk
from typeclass.data.sequence import Sequence, Cons, Nil, zipwith
from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.show import Show
from typeclass.protocols.force import Force

A = TypeVar("A")
B = TypeVar("B")

@dataclass(frozen=True)
class Tree(Applicative[A], Functor[A], Show, Generic[A]):
    value: A
    children: Seq[Tree[A]]

    # ----- Functor ---------------------------------------------------------

    def fmap(self: Tree[A], f: Force[Callable[[A], B]]) -> Tree[B]:
        match self:
            case Tree(value=value, children=children):
                nf = f.force()
                nchildren = children.fmap(Thunk(lambda: lambda tree: tree.fmap(f)))
                return Tree(nf(value), nchildren)

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls: type, value: A) -> Tree[A]:
        return Tree(value, Nil())

    def ap(self: Tree[Callable[[A], B]], fa: Force[Tree[A]]) -> Tree[B]:
        _fa = fa.force()

        match (self, _fa):
            case (Tree(value=f, children=tfs), Tree(value=a, children=txs)):
                return Tree(f(a), zipwith(lambda tf, tx: tf.ap(Thunk(lambda: tx)), tfs, txs))
    
    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        children = ", ".join(repr(child) for child in self.children)
        return f"Tree({self.value!r}, [{children}])"
