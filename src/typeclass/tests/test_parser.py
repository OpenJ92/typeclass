import unittest

from typeclass.data.parser import Parser
from typeclass.interpret.interpreter import interpret
from typeclass.tests.fixtures import parser as fx_parser

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
from typeclass.tests.laws.alternative import (
    alternative_left_identity_expr,
    alternative_right_identity_expr,
    alternative_associativity_expr,
    alternative_some_expr,
    alternative_many_expr,
)


class ParserTestCase(unittest.TestCase):
    def assert_parser_expr_equal(self, lhs, rhs):
        lhs_parser = interpret(lhs, None, None).force()
        rhs_parser = interpret(rhs, None, None).force()

        for s in fx_parser.inputs():
            with self.subTest(input=s):
                self.assertEqual(lhs_parser.run(s), rhs_parser.run(s))


class TestParserFunctor(ParserTestCase):
    def test_functor_identity(self):
        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = functor_identity_expr(value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_functor_composition(self):
        f = lambda x: x + "!"
        g = lambda x: f"[{x}]"

        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = functor_composition_expr(value, f, g)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_functor_replace(self):
        replacement = "x"

        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = functor_replace_expr(value, replacement)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_functor_void(self):
        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = functor_void_expr(value)
                self.assert_parser_expr_equal(lhs, rhs)


class TestParserApplicative(ParserTestCase):
    def test_applicative_identity(self):
        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = applicative_identity_expr(Parser, value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_applicative_homomorphism(self):
        funcs = [
            lambda x: x + 1,
            lambda x: x * 2,
        ]
        xs = [0, 1, 10]

        for f in funcs:
            for x in xs:
                with self.subTest(f=f, x=x):
                    lhs, rhs = applicative_homomorphism_expr(Parser, f, x)
                    self.assert_parser_expr_equal(lhs, rhs)

    def test_applicative_interchange(self):
        function_values = [
            Parser(lambda s: [(lambda x: x + 1, s)]),
            Parser(lambda s: [(lambda x: x * 2, s)]),
        ]
        ys = [0, 1, 10]

        for u in function_values:
            for y in ys:
                with self.subTest(u=u, y=y):
                    lhs, rhs = applicative_interchange_expr(Parser, u, y)
                    self.assert_parser_expr_equal(lhs, rhs)

    def test_applicative_composition(self):
        us = [
            Parser(lambda s: [(lambda x: x + "!", s)]),
            Parser(lambda s: [(lambda x: f"[{x}]", s)]),
        ]
        vs = [
            Parser(lambda s: [(lambda x: x.upper(), s)]),
            Parser(lambda s: [(lambda x: x + x, s)]),
        ]

        for u in us:
            for v in vs:
                for w in fx_parser.values():
                    with self.subTest(u=u, v=v, w=w):
                        lhs, rhs = applicative_composition_expr(Parser, u, v, w)
                        self.assert_parser_expr_equal(lhs, rhs)

    def test_applicative_then_definition(self):
        for fa in fx_parser.values():
            for fb in fx_parser.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_then_expr(fa, fb)
                    self.assert_parser_expr_equal(lhs, rhs)

    def test_applicative_skip_definition(self):
        for fa in fx_parser.values():
            for fb in fx_parser.values():
                with self.subTest(fa=fa, fb=fb):
                    lhs, rhs = applicative_skip_expr(fa, fb)
                    self.assert_parser_expr_equal(lhs, rhs)

    def test_applicative_lifta2_definition(self):
        funcs = [
            lambda a, b: (a, b),
            lambda a, b: f"{a}:{b}",
        ]

        for f in funcs:
            for fa in fx_parser.values():
                for fb in fx_parser.values():
                    with self.subTest(f=f, fa=fa, fb=fb):
                        lhs, rhs = applicative_liftA2_expr(f, fa, fb)
                        self.assert_parser_expr_equal(lhs, rhs)


class TestParserMonad(ParserTestCase):
    def test_monad_left_identity(self):
        xs = [0, 1, 10, "x"]
        funcs = [
            lambda x: Parser(lambda s: [(x, s)]),
            lambda x: Parser(lambda s: [(f"{x}!", s)]),
        ]

        for x in xs:
            for f in funcs:
                with self.subTest(x=x, f=f):
                    lhs, rhs = monad_left_identity_expr(Parser, x, f)
                    self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_right_identity(self):
        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = monad_right_identity_expr(value, Parser)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_associativity(self):
        f = lambda x: Parser(lambda s: [(f"{x}!", s)])
        g = lambda x: Parser(lambda s: [(f"[{x}]", s)])

        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = monad_associativity_expr(value, f, g)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_join_definition(self):
        values = [
            Parser(lambda s: []),
            Parser(lambda s: [(Parser(lambda t: [("x", t)]), s)]),
            Parser(lambda s: [(Parser(lambda t: [(t, "")]), s)]),
        ]

        for value in values:
            with self.subTest(value=value):
                lhs, rhs = monad_join_expr(value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_mthen_definition(self):
        for ma in fx_parser.values():
            for mb in fx_parser.values():
                with self.subTest(ma=ma, mb=mb):
                    lhs, rhs = monad_mthen_expr(ma, mb)
                    self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_rbind_definition(self):
        f = lambda x: Parser(lambda s: [(f"{x}!", s)])

        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = monad_rbind_expr(f, value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_kleisli_definition(self):
        f = lambda x: Parser(lambda s: [(f"{x}!", s)])
        g = lambda x: Parser(lambda s: [(f"[{x}]", s)])
        xs = [0, 1, "x"]

        for x in xs:
            with self.subTest(x=x):
                lhs, rhs = monad_kleisli_expr(f, g, x)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_monad_rkleisli_definition(self):
        f = lambda x: Parser(lambda s: [(f"{x}!", s)])
        g = lambda x: Parser(lambda s: [(f"[{x}]", s)])
        xs = [0, 1, "x"]

        for x in xs:
            with self.subTest(x=x):
                lhs, rhs = monad_rkleisli_expr(f, g, x)
                self.assert_parser_expr_equal(lhs, rhs)


class TestParserAlternative(ParserTestCase):
    def test_alternative_left_identity(self):
        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = alternative_left_identity_expr(Parser, value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_alternative_right_identity(self):
        for value in fx_parser.values():
            with self.subTest(value=value):
                lhs, rhs = alternative_right_identity_expr(Parser, value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_alternative_associativity(self):
        for x in fx_parser.values():
            for y in fx_parser.values():
                for z in fx_parser.values():
                    with self.subTest(x=x, y=y, z=z):
                        lhs, rhs = alternative_associativity_expr(x, y, z)
                        self.assert_parser_expr_equal(lhs, rhs)

    def test_alternative_some_definition(self):
        for value in fx_parser.consuming_values():
            with self.subTest(value=value):
                lhs, rhs = alternative_some_expr(Parser, value)
                self.assert_parser_expr_equal(lhs, rhs)

    def test_alternative_many_definition(self):
        for value in fx_parser.consuming_values():
            with self.subTest(value=value):
                lhs, rhs = alternative_many_expr(Parser, value)
                self.assert_parser_expr_equal(lhs, rhs)


if __name__ == "__main__":
    unittest.main()
