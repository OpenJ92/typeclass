import unittest

from typeclass.data.writer import Writer
from typeclass.data.sequence import Sequence, Cons, Nil
from typeclass.interpret.run import run
from typeclass.tests.fixtures import writer as fx_writer

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

class WriterTestCase(unittest.TestCase):
    def assert_expr_equal(self, lhs, rhs):
        self.assertEqual(
            run(lhs, None, None).force(),
            run(rhs, None, None).force(),
        )


class TestWriterFunctor(WriterTestCase):
    def test_functor_identity(self):
        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + 1
        g = lambda x: x * x

        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = fx_writer.replacement()

        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_expr_equal(lhs, rhs)


class TestWriterApplicative(WriterTestCase):
    def test_applicative_identity(self):
        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Writer(Sequence), value)
                self.assert_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]

        for f in funcs:
            for x in fx_writer.pure_values():
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Writer(Sequence), f, x)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        ys = fx_writer.pure_values()

        for u in fx_writer.function_values():
            for y in ys:
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Writer(Sequence), u, y)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us = [
            Writer(Sequence)(lambda x: x + 1, fx_writer.values()[0].log),
            Writer(Sequence)(lambda x: x * 2, fx_writer.values()[1].log),
        ]
        vs = [
            Writer(Sequence)(lambda x: x - 3, fx_writer.values()[0].log),
            Writer(Sequence)(lambda x: x * x, fx_writer.values()[2].log),
        ]

        for u in us:
            for v in vs:
                for w in fx_writer.values():
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Writer(Sequence), u, v, w)
                        self.assert_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        for fa in fx_writer.values():
            for fb in fx_writer.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        for fa in fx_writer.values():
            for fb in fx_writer.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        funcs = [
            lambda a, b: (a, b),
            lambda a, b: f"{a}:{b}",
        ]
        for f in funcs:
            for fa in fx_writer.values():
                for fb in fx_writer.values():
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_expr_equal(lhs, rhs)

class TestWriterMonad(WriterTestCase):
    def test_monad_left_identity(self):
        funcs = [
            lambda x: Writer(Sequence)(x, Cons("id", Nil())),
            lambda x: Writer(Sequence)(x + 1, Cons("inc", Nil())),
        ]

        for x in [0, 1, 10]:
            for f in funcs:
                with self.subTest(x=x, f=f):
                    lhs, rhs = monad_left_identity_expr(Writer(Sequence), x, f)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_right_identity(self):
        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = monad_right_identity_expr(value, Writer(Sequence))
                self.assert_expr_equal(lhs, rhs)

    def test_monad_associativity(self):
        f = lambda x: Writer(Sequence)(x + 1, Cons("f", Nil()))
        g = lambda x: Writer(Sequence)(x * 2, Cons("g", Nil()))

        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = monad_associativity_expr(value, f, g)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_join_definition(self):
        for value in fx_writer.join_values():
            with self.subTest(value=value):
                lhs, rhs = monad_join_expr(value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_mthen_definition(self):
        for ma in fx_writer.values():
            for mb in fx_writer.values():
                with self.subTest(ma=ma, mb=mb):
                    lhs, rhs = monad_mthen_expr(ma, mb)
                    self.assert_expr_equal(lhs, rhs)

    def test_monad_rbind_definition(self):
        f = lambda x: Writer(Sequence)(x + 1, Cons("rbind", Nil()))

        for value in fx_writer.values():
            with self.subTest(value=value):
                lhs, rhs = monad_rbind_expr(f, value)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_kleisli_definition(self):
        f = lambda x: Writer(Sequence)(x + 1, Cons("f", Nil()))
        g = lambda x: Writer(Sequence)(x * 2, Cons("g", Nil()))

        for x in [0, 1, 10]:
            with self.subTest(x=x):
                lhs, rhs = monad_kleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)

    def test_monad_rkleisli_definition(self):
        f = lambda x: Writer(Sequence)(x + 1, Cons("f", Nil()))
        g = lambda x: Writer(Sequence)(x * 2, Cons("g", Nil()))

        for x in [0, 1, 10]:
            with self.subTest(x=x):
                lhs, rhs = monad_rkleisli_expr(f, g, x)
                self.assert_expr_equal(lhs, rhs)


if __name__ == "__main__":
    unittest.main()
