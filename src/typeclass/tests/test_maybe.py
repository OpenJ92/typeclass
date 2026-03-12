import unittest

from typeclass.data.maybe import Maybe, Just, Nothing
from typeclass.tests.laws.functor import assert_functor_identity, assert_functor_composition, assert_functor_replace, assert_functor_void

class TestMaybe(unittest.TestCase):
    def test_functor_identity(self):
        for value in [Just(10), Nothing()]:
            with self.subTest(value=value):
                assert_functor_identity(value)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x
        for value in [Just(10), Nothing()]:
            with self.subTest(value=value):
                assert_functor_composition(value, f, g)

    def test_functor_replace(self):
        for value in [Just(10), Nothing()]:
            with self.subTest(value=value):
                assert_functor_replace(value, "10")

    def test_functor_void(self):
        for value in [Just(10), Nothing()]:
            with self.subTest(value=value):
                assert_functor_void(value)
