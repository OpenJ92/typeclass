import unittest

from typeclass.interpret.interpreter import interpret
from typeclass.tests.fixtures import reader as fx_reader
from typeclass.tests.laws.functor import (
    functor_identity_expr,
    functor_composition_expr,
    functor_replace_expr,
    functor_void_expr,
)


class ReaderTestCase(unittest.TestCase):
    def assert_reader_expr_equal(self, lhs, rhs):
        lhs_reader = interpret(lhs, None, None).force()
        rhs_reader = interpret(rhs, None, None).force()

        for env in fx_reader.envs():
            with self.subTest(env=env):
                self.assertEqual(lhs_reader.run(env), rhs_reader.run(env))


class TestReaderFunctor(ReaderTestCase):
    def test_functor_identity(self):
        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_reader.replacement()

        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_reader_expr_equal(lhs, rhs)


if __name__ == "__main__":
    unittest.main()
