import unittest

from typeclass.data.automorphism import Automorphism
from typeclass.interpret.run import run
from typeclass.tests.fixtures import automorphism as fx_automorphism

from typeclass.tests.laws.semigroup import (
    semigroup_associativity_expr,
)
from typeclass.tests.laws.monoid import (
    monoid_left_identity_expr,
    monoid_right_identity_expr,
)
from typeclass.tests.laws.group import (
    group_left_inverse_expr,
    group_right_inverse_expr,
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
from typeclass.tests.laws.groupoid import (
    groupoid_left_invert_expr,
    groupoid_right_invert_expr,
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


class AutomorphismTestCase(unittest.TestCase):
    def assert_automorphism_expr_equal(self, lhs, rhs, inputs=None):
        left = run(lhs, None, None).force()
        right = run(rhs, None, None).force()

        if inputs is None:
            inputs = fx_automorphism.inputs()

        for x in inputs:
            with self.subTest(input=x):
                self.assertEqual(left(x), right(x))


class TestAutomorphismSemigroup(AutomorphismTestCase):
    def test_semigroup_associativity(self):
        for f, g, h in fx_automorphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroup_associativity_expr(f, g, h)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismMonoid(AutomorphismTestCase):
    def test_monoid_left_identity(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = monoid_left_identity_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_monoid_right_identity(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = monoid_right_identity_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismGroup(AutomorphismTestCase):
    def test_group_left_inverse(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = group_left_inverse_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_group_right_inverse(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = group_right_inverse_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismSemigroupoid(AutomorphismTestCase):
    def test_semigroupoid_associativity(self):
        for f, g, h in fx_automorphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroupoid_associativity_expr(f, g, h)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_semigroupoid_rassociativity(self):
        for f, g, h in fx_automorphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroupoid_rassociativity_expr(f, g, h)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_semigroupoid_compose_rcompose(self):
        for f, g in fx_automorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = semigroupoid_compose_rcompose_expr(f, g)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismCategory(AutomorphismTestCase):
    def test_category_left_identity(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_left_identity_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_category_right_identity(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_right_identity_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_category_left_ridentity(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_left_ridentity_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_category_right_ridentity(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_right_ridentity_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismGroupoid(AutomorphismTestCase):
    def test_groupoid_left_invert(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = groupoid_left_invert_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_groupoid_right_invert(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = groupoid_right_invert_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismArrow(AutomorphismTestCase):
    def test_arrow_identity(self):
        lhs, rhs = arrow_identity_expr(Automorphism)
        self.assert_automorphism_expr_equal(lhs, rhs)

    def test_arrow_composition(self):
        for f, g in fx_automorphism.composition_pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrow_composition_expr(Automorphism, f, g)
                self.assert_automorphism_expr_equal(lhs, rhs)

    def test_arrow_first_identity(self):
        lhs, rhs = arrow_first_identity_expr(Automorphism)
        self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.pair_inputs())

    def test_arrow_first_composition(self):
        for f, g in fx_automorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrow_first_composition_expr(Automorphism, f, g)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.pair_inputs())

    def test_arrow_second(self):
        for value in fx_automorphism.values():
            with self.subTest(value=value):
                lhs, rhs = arrow_second_expr(Automorphism, value)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.pair_inputs())

    def test_arrow_split(self):
        for value1, value2 in fx_automorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrow_split_expr(Automorphism, value1, value2)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.pair_inputs())

    def test_arrow_fanout(self):
        for value1, value2 in fx_automorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrow_fanout_expr(Automorphism, value1, value2)
                self.assert_automorphism_expr_equal(lhs, rhs)


class TestAutomorphismArrowChoice(AutomorphismTestCase):
    def test_arrowchoice_left_naturality(self):
        for f in fx_automorphism.arrow_functions():
            with self.subTest(f=f):
                lhs, rhs = arrowchoice_left_naturality_expr(Automorphism, f)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_right_naturality(self):
        for f in fx_automorphism.arrow_functions():
            with self.subTest(f=f):
                lhs, rhs = arrowchoice_right_naturality_expr(Automorphism, f)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_left_identity(self):
        lhs, rhs = arrowchoice_left_identity_expr(Automorphism)
        self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_right_identity(self):
        lhs, rhs = arrowchoice_right_identity_expr(Automorphism)
        self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_left_composition(self):
        for f, g in fx_automorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrowchoice_left_composition_expr(Automorphism, f, g)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_right_composition(self):
        for f, g in fx_automorphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrowchoice_right_composition_expr(Automorphism, f, g)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_split_choice(self):
        for value1, value2 in fx_automorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrowchoice_split_choice_expr(Automorphism, value1, value2)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())

    def test_arrowchoice_fanin(self):
        for value1, value2 in fx_automorphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrowchoice_fanin_expr(Automorphism, value1, value2)
                self.assert_automorphism_expr_equal(lhs, rhs, inputs=fx_automorphism.either_inputs())


class TestAutomorphismArrowApply(AutomorphismTestCase):
    def test_arrowapply_arr_app(self):
        for f in fx_automorphism.arrow_functions():
            with self.subTest(f=f):
                lhs, rhs = arrowapply_arr_app_expr(Automorphism, f)
                self.assert_automorphism_expr_equal(lhs, rhs)
