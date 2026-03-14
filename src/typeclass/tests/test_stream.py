import unittest

from typeclass.data.stream import Stream
from typeclass.data.stream.lib import take
from typeclass.interpret.interpreter import interpret
from typeclass.tests.fixtures import stream as fx_stream

from typeclass.tests.laws.functor import (
    functor_identity_expr,
    functor_composition_expr,
    functor_replace_expr,
    functor_void_expr,
)
from typeclass.tests.laws.applicative import (
    applicative_identity_expr,
    applicative_homomorphism_expr,
    applicative_interchange_expr,
    applicative_composition_expr,
    applicative_then_expr,
    applicative_skip_expr,
    applicative_liftA2_expr,
)
from typeclass.tests.laws.comonad import (
    comonad_left_identity_expr,
    comonad_right_identity_expr,
    comonad_associativity_expr,
    comonad_extend_expr,
    comonad_duplicate_expr,
    comonad_extract_duplicate_expr,
    comonad_duplicate_associativity_expr,
)


class StreamTestCase(unittest.TestCase):
    def assert_expr_equal(self, lhs, rhs, prefix: int | None = None):
        self.assertEqual(
            interpret(lhs, None, None).force(),
            interpret(rhs, None, None).force(),
        )


class TestStreamFunctor(StreamTestCase):
    def test_functor_identity(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_stream.replacement()

        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_expr_equal(lhs, rhs)


class TestStreamApplicative(StreamTestCase):
    def test_applicative_identity(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Stream, value)
                self.assert_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]

        for f in funcs:
            for x in fx_stream.pure_values():
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Stream, f, x)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        for u in fx_stream.function_values():
            for y in fx_stream.pure_values():
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Stream, u, y)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us, vs = fx_stream.composition_function_values()

        for u in us:
            for v in vs:
                for w in fx_stream.values():
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Stream, u, v, w)
                        self.assert_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        for fa in fx_stream.values():
            for fb in fx_stream.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        for fa in fx_stream.values():
            for fb in fx_stream.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        for f in fx_stream.binary_functions():
            for fa in fx_stream.values():
                for fb in fx_stream.values():
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_expr_equal(lhs, rhs)


class TestStreamComonad(StreamTestCase):
    def test_comonad_left_identity(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = comonad_left_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_right_identity(self):
        for value in fx_stream.values():
            for f in fx_stream.comonad_functions():
                with self.subTest(value=value, f=f):
                    lhs, rhs = comonad_right_identity_expr(value, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_comonad_associativity(self):
        f, g = fx_stream.comonad_functions()[:2]

        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = comonad_associativity_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_extend_definition(self):
        for value in fx_stream.values():
            for f in fx_stream.comonad_functions():
                with self.subTest(value=value, f=f):
                    lhs, rhs = comonad_extend_expr(value, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_comonad_duplicate_definition(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = comonad_duplicate_expr(value)
                self.assert_expr_equal(lhs, rhs, prefix=8)

    def test_comonad_extract_duplicate_definition(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = comonad_extract_duplicate_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_duplicate_associativity(self):
        for value in fx_stream.values():
            with self.subTest(value=value):
                lhs, rhs = comonad_duplicate_associativity_expr(value)
                self.assert_expr_equal(lhs, rhs, prefix=6)


if __name__ == "__main__":
    unittest.main()
