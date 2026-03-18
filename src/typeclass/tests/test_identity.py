import unittest

from typeclass.data.identity import Identity
from typeclass.interpret.run import run
from typeclass.tests.fixtures import identity as fx_identity

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
from typeclass.tests.laws.comonad import (
    comonad_left_identity_expr,
    comonad_right_identity_expr,
    comonad_associativity_expr,
    comonad_extend_expr,
    comonad_duplicate_expr,
    comonad_extract_duplicate_expr,
    comonad_duplicate_associativity_expr,
)


class IdentityTestCase(unittest.TestCase):
    def assert_expr_equal(self, lhs, rhs):
        self.assertEqual(
            run(lhs, None, None).force(),
            run(rhs, None, None).force(),
        )


class TestIdentityFunctor(IdentityTestCase):
    def test_functor_identity(self):
        for value in fx_identity.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_identity.values():
            if not isinstance(value.value, int):
                continue
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_identity.replacement()

        for value in fx_identity.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_identity.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_expr_equal(lhs, rhs)


class TestIdentityApplicative(IdentityTestCase):
    def test_applicative_identity(self):
        for value in fx_identity.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Identity, value)
                self.assert_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]

        for f in funcs:
            for x in fx_identity.pure_values():
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Identity, f, x)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        for u in fx_identity.function_values():
            for y in fx_identity.pure_values():
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Identity, u, y)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us, vs = fx_identity.composition_function_values()

        for u in us:
            for v in vs:
                for w in [Identity(x) for x in fx_identity.pure_values()]:
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Identity, u, v, w)
                        self.assert_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        for fa in fx_identity.values():
            for fb in fx_identity.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        for fa in fx_identity.values():
            for fb in fx_identity.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        int_values = [Identity(x) for x in fx_identity.pure_values()]

        for f in fx_identity.binary_functions():
            for fa in int_values:
                for fb in int_values:
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_expr_equal(lhs, rhs)


class TestIdentityMonad(IdentityTestCase):
    def test_monad_left_identity(self):
        for x in fx_identity.pure_values():
            for f in fx_identity.monad_functions():
                with self.subTest(x=x, f=f):
                    lhs, rhs = monad_left_identity_expr(Identity, x, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_right_identity(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = monad_right_identity_expr(value, Identity)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_associativity(self):
        funcs = fx_identity.monad_functions()
        f, g = funcs[0], funcs[1]

        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = monad_associativity_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_join_definition(self):
        for value in fx_identity.join_values():
            with self.subTest(value=value):
                lhs, rhs = monad_join_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_mthen_definition(self):
        vals = [Identity(x) for x in fx_identity.pure_values()]

        for ma in vals:
            for mb in vals:
                with self.subTest(ma=ma, mb=mb):
                    lhs, rhs = monad_mthen_expr(ma, mb)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_rbind_definition(self):
        f = fx_identity.monad_functions()[0]

        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = monad_rbind_expr(f, value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_kleisli_definition(self):
        f, g = fx_identity.monad_functions()[:2]

        for x in fx_identity.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_kleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_rkleisli_definition(self):
        f, g = fx_identity.monad_functions()[:2]

        for x in fx_identity.pure_values():
            with self.subTest(x=x):
                lhs, rhs = monad_rkleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)


class TestIdentityComonad(IdentityTestCase):
    def test_comonad_left_identity(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = comonad_left_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_right_identity(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            for f in fx_identity.comonad_functions():
                with self.subTest(value=value, f=f):
                    lhs, rhs = comonad_right_identity_expr(value, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_comonad_associativity(self):
        f, g = fx_identity.comonad_functions()[:2]

        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = comonad_associativity_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_extend_definition(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            for f in fx_identity.comonad_functions():
                with self.subTest(value=value, f=f):
                    lhs, rhs = comonad_extend_expr(value, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_comonad_duplicate_definition(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = comonad_duplicate_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_extract_duplicate_definition(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = comonad_extract_duplicate_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_comonad_duplicate_associativity(self):
        for value in [Identity(x) for x in fx_identity.pure_values()]:
            with self.subTest(value=value):
                lhs, rhs = comonad_duplicate_associativity_expr(value)
                self.assert_expr_equal(lhs, rhs)

