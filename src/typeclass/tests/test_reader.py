import unittest

from typeclass.data.reader import Reader
from typeclass.interpret.run import run
from typeclass.tests.fixtures import reader as fx_reader

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
from typeclass.tests.laws.monad import (
    monad_left_identity_expr,
    monad_right_identity_expr,
    monad_associativity_expr,
    monad_join_expr,
    monad_mthen_expr,
    monad_rbind_expr,
    monad_kleisli_expr,
    monad_rkleisli_expr,
)


class ReaderTestCase(unittest.TestCase):
    def assert_reader_expr_equal(self, lhs, rhs):
        lhs_reader = run(lhs, None, None).force()
        rhs_reader = run(rhs, None, None).force()

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


class TestReaderApplicative(ReaderTestCase):
    def test_applicative_identity(self):
        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Reader, value)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]

        for f in funcs:
            for x in fx_reader.pure_values():
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Reader, f, x)
                    self.assert_reader_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        for u in fx_reader.function_values():
            for y in fx_reader.pure_values():
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Reader, u, y)
                    self.assert_reader_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us = [
            Reader(lambda r: (lambda x: x + r)),
            Reader(lambda r: (lambda x: x * (r + 1))),
        ]
        vs = [
            Reader(lambda r: (lambda x: x - r)),
            Reader(lambda r: (lambda x: x + 2)),
        ]

        for u in us:
            for v in vs:
                for w in fx_reader.values():
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Reader, u, v, w)
                        self.assert_reader_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        for fa in fx_reader.values():
            for fb in fx_reader.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_reader_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        for fa in fx_reader.values():
            for fb in fx_reader.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_reader_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        for f in fx_reader.binary_functions():
            for fa in fx_reader.values():
                for fb in fx_reader.values():
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_reader_expr_equal(lhs, rhs)


class TestReaderMonad(ReaderTestCase):
    def test_monad_left_identity(self):
        for x in fx_reader.pure_values():
            for f in fx_reader.monad_functions():
                with self.subTest(x=x, f=f):
                    lhs, rhs = monad_left_identity_expr(Reader, x, f)
                    self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_right_identity(self):
        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = monad_right_identity_expr(value, Reader)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_associativity(self):
        funcs = fx_reader.monad_functions()
        f, g = funcs[0], funcs[1]

        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = monad_associativity_expr(value, f, g)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_join_definition(self):
        for value in fx_reader.join_values():
            with self.subTest(value=value):
                lhs, rhs = monad_join_expr(value)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_mthen_definition(self):
        for ma in fx_reader.values():
            for mb in fx_reader.values():
                with self.subTest(ma=ma, mb=mb):
                    lhs, rhs = monad_mthen_expr(ma, mb)
                    self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_rbind_definition(self):
        f = fx_reader.monad_functions()[0]

        for value in fx_reader.values():
            with self.subTest(value=value):
                lhs, rhs = monad_rbind_expr(f, value)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_kleisli_definition(self):
        f, g = fx_reader.monad_functions()[:2]

        for x in fx_reader.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_kleisli_expr(f, g, x)
                self.assert_reader_expr_equal(lhs, rhs)

    def test_monad_rkleisli_definition(self):
        f, g = fx_reader.monad_functions()[:2]

        for x in fx_reader.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_rkleisli_expr(f, g, x)
                self.assert_reader_expr_equal(lhs, rhs)


if __name__ == "__main__":
    unittest.main()
