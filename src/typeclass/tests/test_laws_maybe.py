import unittest
from typeclass.data.maybe import Maybe, Just
from typeclass.laws.functor import assert_functor_laws
from typeclass.laws.applicative import assert_applicative_laws

class TestMaybeLaws(unittest.TestCase):
    def test_functor_laws(self):
        assert_functor_laws(Just(10), lambda x: x + 1, lambda y: y * 2)

    def test_applicative_laws(self):
        assert_applicative_laws(Maybe, Just(42), lambda x: x + 1, lambda y: y * 3, 7)

