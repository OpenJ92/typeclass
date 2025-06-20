from typeclass.laws.functor import assert_functor_laws
from typeclass.data.maybe import \
        ( Maybe , Just , Nothing
        , is_just, is_nothing, from_maybe, maybe, cat_maybes, map_maybe
        )


print(is_just(Just(5)))     # True
print(is_nothing(Nothing()))  # True
print(from_maybe(0, Just(10)))  # 10
print(from_maybe(0, Nothing()))  # 0
print(maybe("nope", str, Just(3)))  # "3"
print(maybe("nope", str, Nothing()))  # "nope"

ms = [Just(1), Nothing(), Just(3)]
print(cat_maybes(ms))  # [1, 3]

def safe_even(x: int) -> Maybe[int]:
    return Just(x) if x % 2 == 0 else Nothing()

print(map_maybe(safe_even, range(5)))  # [0, 2, 4]

print(Just(3) == Just(3))     # True
print(Just(3) == Just(4))     # False
print(Nothing() == Nothing()) # True
print(Just(3) == Nothing())   # False

assert_functor_laws(Just(10), lambda x: x + 10, lambda x: x * 2)
assert_functor_laws(Nothing(), lambda x: x + 10, lambda x: x * 2)

print(Just(lambda x: x * 2).ap(Just(5)))


from typeclass.syntax.symbols import fmap, replace, ap, pure, then, skip
## Functor fmap and Applicative ap in use. Infix class
print((Just(10) |fmap| (lambda x: lambda y: x + y)) |ap| Just(9))
print(Maybe |pure| (lambda x: lambda y: x + y) |ap| Just(10) |ap| Just(9))

print(Just("a") |then| Just("b"))
print(Just("a") |skip| Just("b"))

print(Nothing() |then| Just("b"))
print(Just("a") |skip| Nothing())

print(Nothing() |then| Nothing())
print(Nothing() |skip| Nothing())

