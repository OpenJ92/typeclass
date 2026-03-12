import unittest

from typeclass.interpret.interpreter import interpret
from typeclass.tests.fixtures import sequence as fx_sequence
from typeclass.tests.laws.functor import (
    functor_identity_expr,
    functor_composition_expr,
    functor_replace_expr,
    functor_void_expr,
)


class SequenceTestCase(unittest.TestCase):
    def assert_expr_equal(self, lhs, rhs):
        self.assertEqual(
            interpret(lhs, None, None).force(),
            interpret(rhs, None, None).force(),
        )


class TestSequenceFunctor(SequenceTestCase):
    def test_functor_identity(self):
        for value in fx_sequence.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_sequence.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_sequence.replacement()

        for value in fx_sequence.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_sequence.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_expr_equal(lhs, rhs)


if __name__ == "__main__":
    unittest.main()
