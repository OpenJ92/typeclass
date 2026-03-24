# typeclass/tests/test_endomorphism.py

import unittest

from typeclass.data.endomorphism import Endomorphism
from typeclass.interpret.run import run
from typeclass.tests.fixtures import endomorphism as fx_endomorphism

from typeclass.tests.laws.semigroup import (
    semigroup_associativity_expr,
)
from typeclass.tests.laws.monoid import (
    monoid_left_identity_expr,
    monoid_right_identity_expr,
)
from typeclass.tests.laws.semigroupoid import (
    semigroupoid_associativity_expr,
    semigroupoid_rassociativity_expr,
    semigroupoid_compose_rcompose_expr,
)
from typeclass.tests.laws.category import (
    category_left_identity_expr,
    category_right_identity_expr,
    category_left_ridentity_expr,
    category_right_ridentity_expr,
)
from typeclass.tests.laws.arrow import (
    arrow_identity_expr,
    arrow_composition_expr,
    arrow_first_identity_expr,
    arrow_first_composition_expr,
    arrow_second_expr,
    arrow_split_expr,
    arrow_fanout_expr,
)
from typeclass.tests.laws.arrowchoice import (
    arrowchoice_left_naturality_expr,
    arrowchoice_right_naturality_expr,
    arrowchoice_left_identity_expr,
    arrowchoice_right_identity_expr,
    arrowchoice_left_composition_expr,
    arrowchoice_right_composition_expr,
    arrowchoice_split_choice_expr,
    arrowchoice_fanin_expr,
)
from typeclass.tests.laws.arrowapply import (
    arrowapply_arr_app_expr,
)


class EndomorphismTestCase(unittest.TestCase):
    def assert_endomorphism_expr_equal(self, lhs, rhs, inputs=None):
        left = run(lhs, None, None).force()
        right = run(rhs, None, None).force()

        if inputs is None:
            inputs = fx_endomorphism.inputs()

        for x in inputs:
            with self.subTest(input=x):
                self.assertEqual(left(x), right(x))


class TestEndomorphismSemigroup(EndomorphismTestCase):
    def test_semigroup_associativity(self):
        for f, g, h in fx_endomorphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroup_associativity_expr(f, g, h)
                self.assert_endomorphism_expr_equal(lhs, rhs)


class TestEndomorphismMonoid(EndomorphismTestCase):
    def test_monoid_left_identity(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = monoid_left_identity_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_monoid_right_identity(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = monoid_right_identity_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs)


class TestEndomorphismSemigroupoid(EndomorphismTestCase):
    def test_semigroupoid_associativity(self):
        for f, g, h in fx_endomorphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroupoid_associativity_expr(f, g, h)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_semigroupoid_rassociativity(self):
        for f, g, h in fx_endomorphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroupoid_rassociativity_expr(f, g, h)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_semigroupoid_compose_rcompose(self):
        for f, g in fx_endomorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = semigroupoid_compose_rcompose_expr(f, g)
                self.assert_endomorphism_expr_equal(lhs, rhs)


class TestEndomorphismCategory(EndomorphismTestCase):
    def test_category_left_identity(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_left_identity_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_category_right_identity(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_right_identity_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_category_left_ridentity(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_left_ridentity_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_category_right_ridentity(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_right_ridentity_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs)


class TestEndomorphismArrow(EndomorphismTestCase):
    def test_arrow_identity(self):
        lhs, rhs = arrow_identity_expr(Endomorphism)
        self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_arrow_composition(self):
        for f, g in fx_endomorphism.composition_pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrow_composition_expr(Endomorphism, f, g)
                self.assert_endomorphism_expr_equal(lhs, rhs)

    def test_arrow_first_identity(self):
        lhs, rhs = arrow_first_identity_expr(Endomorphism)
        self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.pair_inputs())

    def test_arrow_first_composition(self):
        for f, g in fx_endomorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrow_first_composition_expr(Endomorphism, f, g)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.pair_inputs())

    def test_arrow_second(self):
        for value in fx_endomorphism.values():
            with self.subTest(value=value):
                lhs, rhs = arrow_second_expr(Endomorphism, value)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.pair_inputs())

    def test_arrow_split(self):
        for value1, value2 in fx_endomorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrow_split_expr(Endomorphism, value1, value2)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.pair_inputs())

    def test_arrow_fanout(self):
        for value1, value2 in fx_endomorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrow_fanout_expr(Endomorphism, value1, value2)
                self.assert_endomorphism_expr_equal(lhs, rhs)


class TestEndomorphismArrowChoice(EndomorphismTestCase):
    def test_arrowchoice_left_naturality(self):
        for f in fx_endomorphism.arrow_functions():
            with self.subTest(f=f):
                lhs, rhs = arrowchoice_left_naturality_expr(Endomorphism, f)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_right_naturality(self):
        for f in fx_endomorphism.arrow_functions():
            with self.subTest(f=f):
                lhs, rhs = arrowchoice_right_naturality_expr(Endomorphism, f)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_left_identity(self):
        lhs, rhs = arrowchoice_left_identity_expr(Endomorphism)
        self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_right_identity(self):
        lhs, rhs = arrowchoice_right_identity_expr(Endomorphism)
        self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_left_composition(self):
        for f, g in fx_endomorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrowchoice_left_composition_expr(Endomorphism, f, g)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_right_composition(self):
        for f, g in fx_endomorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrowchoice_right_composition_expr(Endomorphism, f, g)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_split_choice(self):
        for value1, value2 in fx_endomorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrowchoice_split_choice_expr(Endomorphism, value1, value2)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())

    def test_arrowchoice_fanin(self):
        for value1, value2 in fx_endomorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrowchoice_fanin_expr(Endomorphism, value1, value2)
                self.assert_endomorphism_expr_equal(lhs, rhs, inputs=fx_endomorphism.either_inputs())


class TestEndomorphismArrowApply(EndomorphismTestCase):
    def test_arrowapply_arr_app(self):
        for f in fx_endomorphism.arrow_functions():
            with self.subTest(f=f):
                lhs, rhs = arrowapply_arr_app_expr(Endomorphism, f)
                self.assert_endomorphism_expr_equal(lhs, rhs)
