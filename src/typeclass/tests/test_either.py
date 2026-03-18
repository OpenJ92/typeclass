import unittest

from typeclass.data.either import Either, Left, Right
from typeclass.interpret.run import run
from typeclass.tests.fixtures import either as fx_either

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


class EitherTestCase(unittest.TestCase):
    def assert_expr_equal(self, lhs, rhs):
        self.assertEqual(
            run(lhs, None, None).force(),
            run(rhs, None, None).force(),
        )


class TestEitherFunctor(EitherTestCase):
    def test_functor_identity(self):
        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_either.replacement()

        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_expr_equal(lhs, rhs)


class TestEitherApplicative(EitherTestCase):
    def test_applicative_identity(self):
        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Either, value)
                self.assert_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]

        for f in funcs:
            for x in fx_either.pure_values():
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Either, f, x)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        for u in fx_either.function_values():
            for y in fx_either.pure_values():
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Either, u, y)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us, vs = fx_either.composition_function_values()

        for u in us:
            for v in vs:
                for w in [Right(x) for x in fx_either.pure_values()] + [Left("w-left")]:
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Either, u, v, w)
                        self.assert_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        vals = fx_either.values()

        for fa in vals:
            for fb in vals:
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        vals = fx_either.values()

        for fa in vals:
            for fb in vals:
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        vals = [Right(x) for x in fx_either.pure_values()] + [Left("fa-left")]

        for f in fx_either.binary_functions():
            for fa in vals:
                for fb in vals:
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_expr_equal(lhs, rhs)


class TestEitherMonad(EitherTestCase):
    def test_monad_left_identity(self):
        funcs = fx_either.monad_functions()[:3]

        for x in fx_either.pure_values():
            for f in funcs:
                with self.subTest(x=x, f=f):
                    lhs, rhs = monad_left_identity_expr(Either, x, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_right_identity(self):
        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = monad_right_identity_expr(value, Either)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_associativity(self):
        funcs = fx_either.monad_functions()
        f, g = funcs[0], funcs[1]

        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = monad_associativity_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_join_definition(self):
        for value in fx_either.join_values():
            with self.subTest(value=value):
                lhs, rhs = monad_join_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_mthen_definition(self):
        vals = fx_either.values()

        for ma in vals:
            for mb in vals:
                with self.subTest(ma=ma, mb=mb):
                    lhs, rhs = monad_mthen_expr(ma, mb)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_rbind_definition(self):
        f = fx_either.monad_functions()[0]

        for value in fx_either.values():
            with self.subTest(value=value):
                lhs, rhs = monad_rbind_expr(f, value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_kleisli_definition(self):
        f, g = fx_either.monad_functions()[:2]

        for x in fx_either.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_kleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_rkleisli_definition(self):
        f, g = fx_either.monad_functions()[:2]

        for x in fx_either.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_rkleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)

