from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from typeclass.protocols.functor import Functor
from typeclass.protocols.applicative import Applicative
from typeclass.protocols.monad import Monad

A = TypeVar("A")
B = TypeVar("B")
Seed = int

MASK64 = (1 << 64) - 1

def _next_u64(seed: Seed) -> tuple[int, Seed]:
    # SplitMix64 step
    z = (seed + 0x9E3779B97F4A7C15) & MASK64
    x = z
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK64
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK64
    x = x ^ (x >> 31)
    return x & MASK64, z

def _u64_to_unit(x: int) -> float:
    # map 53 high bits to [0,1)
    return ((x >> 11) & ((1 << 53) - 1)) / float(1 << 53)

@dataclass(frozen=True)
class Random(Generic[A]):
    run: Callable[[Seed], tuple[A, Seed]]

    # --- Functor -----------------------------------------------------------

    def fmap(self, f: Callable[[A], B]) -> Random[B]:
        def inner(seed: Seed) -> tuple[B, Seed]:
            a, s1 = self.run(seed)
            return f(a), s1
        return Random(inner)

    # --- Applicative -------------------------------------------------------

    @classmethod
    def pure(cls, a: A) -> Random[A]:
        return Random(lambda seed: (a, seed))

    def ap(self: Random[Callable[[A], B]], ra: Random[A]) -> Random[B]:
        def inner(seed: Seed) -> tuple[B, Seed]:
            fn, s1 = self.run(seed)
            a, s2 = ra.run(s1)
            return fn(a), s2
    return Random(inner)

    # --- Monad -------------------------------------------------------------

    def bind(self, k: Callable[[A], Random[B]]) -> Random[B]:
        def inner(seed: Seed) -> tuple[B, Seed]:
            a, s1 = self.run(seed)
            return k(a).run(s1)
        return Random(inner)

    # handy primitives
    @staticmethod
    def u64() -> Random[int]:
        return Random(_next_u64)

    @staticmethod
    def unit() -> Random[float]:
        return Random.u64().fmap(_u64_to_unit)

    @staticmethod
    def int(lo: int, hi: int) -> Random[int]:
        # inclusive lo, exclusive hi
        span = hi - lo
        return Random.u64().fmap(lambda x: lo + (x % span))

    @staticmethod
    def choice(xs: list[A]) -> Random[A]:
        if not xs:
            raise ValueError("choice on empty list")
        return Random.int(0, len(xs)).fmap(lambda i: xs[i])
