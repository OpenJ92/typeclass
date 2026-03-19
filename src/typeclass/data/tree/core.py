from dataclasses import dataclass
from typing import Generic, TypeVar, Callable

from typeclass.data.thunk import Thunk
from typeclass.data.sequence import Sequence, concat
from typeclass.typeclasses.functor import Functor
from typeclass.typeclasses.applicative import Applicative
from typeclass.typeclasses.monad import Monad
from typeclass.typeclasses.show import Show
from typeclass.typeclasses.eq import Eq
from typeclass.typeclasses.force import Force

A = TypeVar("A")
B = TypeVar("B")

@dataclass(frozen=True)
class Tree(Monad[A], Applicative[A], Functor[A], Show, Eq, Generic[A]):
    value: A
    children: Sequence[Tree[A]]

    # ----- Functor ---------------------------------------------------------

    def fmap(self: Tree[A], f: Force[Callable[[A], B]]) -> Tree[B]:
        match self:
            case Tree(value=value, children=children):
                nf = f.force()
                nchildren = children.fmap(Thunk(lambda: lambda tree: tree.fmap(f)))
                return Tree(nf(value), nchildren)

    # ----- Applicative -----------------------------------------------------

    @classmethod
    def pure(cls, value: A) -> Tree[A]:
        return Tree(value, Sequence(()))

    def ap(self: Tree[Callable[[A], B]], fa: Force[Tree[A]]) -> Tree[B]:
        xs = fa.force()

        return self.bind(
            Thunk(
                lambda: lambda f:
                    xs.fmap(
                        Thunk(lambda: lambda x: f(x))
                    )
            )
        )

    # ----- Monad ------------------------------------------------------------

    def bind(self: Tree[A], f: Force[Callable[[A], Tree[B]]]) -> Tree[B]:
        nf = f.force()

        match self:
            case Tree(value=value, children=children):

                rewritten = nf(value)

                rebound_children = children.fmap(
                    Thunk(
                        lambda: lambda child:
                            child.bind(Thunk(lambda: nf))
                    )
                )

                return Tree(
                    rewritten.value,
                    concat(rewritten.children, rebound_children)
                )
    
    # ----- Show ------------------------------------------------------------

    def __repr__(self) -> str:
        children = ", ".join(repr(child) for child in self.children)
        return f"Tree({self.value!r}, [{children}])"

    # ----- Eq --------------------------------------------------------------

    def __eq__(self: Tree[A], other: Tree[A]) -> bool:
        match (self, other):
            case (Tree(c, cs), Tree(d, ds)):
                return c == d and cs == ds
            case _:
                return False

