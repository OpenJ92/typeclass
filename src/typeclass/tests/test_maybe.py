import unittest

from typeclass.data.maybe import Just, Nothing, Maybe
from typeclass.interpret.run import run
from typeclass.tests.fixtures import maybe as fx_maybe

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


class MaybeTestCase(unittest.TestCase):
    def assert_expr_equal(self, lhs, rhs):
        self.assertEqual(
            run(lhs, None, None).force(),
            run(rhs, None, None).force(),
        )


class TestMaybeFunctor(MaybeTestCase):
    def test_functor_identity(self):
        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_maybe.replacement()

        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_expr_equal(lhs, rhs)


class TestMaybeApplicative(MaybeTestCase):
    def test_applicative_identity(self):
        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Maybe, value)
                self.assert_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]

        for f in funcs:
            for x in fx_maybe.pure_values():
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Maybe, f, x)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        for u in fx_maybe.function_values():
            for y in fx_maybe.pure_values():
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Maybe, u, y)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us = [
            Just(lambda x: x + 1),
            Just(lambda x: x * 2),
            Nothing(),
        ]
        vs = [
            Just(lambda x: x - 3),
            Just(lambda x: x * x),
            Nothing(),
        ]

        for u in us:
            for v in vs:
                for w in fx_maybe.values():
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Maybe, u, v, w)
                        self.assert_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        for fa in fx_maybe.values():
            for fb in fx_maybe.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        for fa in fx_maybe.values():
            for fb in fx_maybe.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        for f in fx_maybe.binary_functions():
            for fa in fx_maybe.values():
                for fb in fx_maybe.values():
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_expr_equal(lhs, rhs)


class TestMaybeMonad(MaybeTestCase):
    def test_monad_left_identity(self):
        for x in fx_maybe.pure_values():
            for f in fx_maybe.monad_functions():
                with self.subTest(x=x, f=f):
                    lhs, rhs = monad_left_identity_expr(Maybe, x, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_right_identity(self):
        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = monad_right_identity_expr(value, Maybe)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_associativity(self):
        f, g = fx_maybe.monad_functions()[:2]

        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = monad_associativity_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_join_definition(self):
        for value in fx_maybe.join_values():
            with self.subTest(value=value):
                lhs, rhs = monad_join_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_mthen_definition(self):
        for ma in fx_maybe.values():
            for mb in fx_maybe.values():
                with self.subTest(ma=ma, mb=mb):
                    lhs, rhs = monad_mthen_expr(ma, mb)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_rbind_definition(self):
        f = fx_maybe.monad_functions()[0]

        for value in fx_maybe.values():
            with self.subTest(value=value):
                lhs, rhs = monad_rbind_expr(f, value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_kleisli_definition(self):
        f, g = fx_maybe.monad_functions()[:2]

        for x in fx_maybe.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_kleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_rkleisli_definition(self):
        f, g = fx_maybe.monad_functions()[:2]

        for x in fx_maybe.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_rkleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)


if __name__ == "__main__":
    unittest.main()
