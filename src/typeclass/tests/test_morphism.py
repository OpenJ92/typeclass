# typeclass/tests/test_morphism.py

import unittest

from typeclass.data.morphism import Morphism
from typeclass.interpret.run import run
from typeclass.tests.fixtures import morphism as fx_morphism

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


class MorphismTestCase(unittest.TestCase):
    def assert_morphism_expr_equal(self, lhs, rhs, inputs=None):
        left = run(lhs, None, None).force()
        right = run(rhs, None, None).force()

        if inputs is None:
            inputs = fx_morphism.inputs()

        for x in inputs:
            with self.subTest(input=x):
                self.assertEqual(left(x), right(x))


class TestMorphismSemigroupoid(MorphismTestCase):
    def test_semigroupoid_associativity(self):
        for f, g, h in fx_morphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroupoid_associativity_expr(f, g, h)
                self.assert_morphism_expr_equal(lhs, rhs)

    def test_semigroupoid_rassociativity(self):
        for f, g, h in fx_morphism.triples():
            with self.subTest(f=f, g=g, h=h):
                lhs, rhs = semigroupoid_rassociativity_expr(f, g, h)
                self.assert_morphism_expr_equal(lhs, rhs)

    def test_semigroupoid_compose_rcompose(self):
        for f, g in fx_morphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = semigroupoid_compose_rcompose_expr(f, g)
                self.assert_morphism_expr_equal(lhs, rhs)


class TestMorphismCategory(MorphismTestCase):
    def test_category_left_identity(self):
        for value in fx_morphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_left_identity_expr(Morphism, value)
                self.assert_morphism_expr_equal(lhs, rhs)

    def test_category_right_identity(self):
        for value in fx_morphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_right_identity_expr(Morphism, value)
                self.assert_morphism_expr_equal(lhs, rhs)

    def test_category_left_ridentity(self):
        for value in fx_morphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_left_ridentity_expr(Morphism, value)
                self.assert_morphism_expr_equal(lhs, rhs)

    def test_category_right_ridentity(self):
        for value in fx_morphism.values():
            with self.subTest(value=value):
                lhs, rhs = category_right_ridentity_expr(Morphism, value)
                self.assert_morphism_expr_equal(lhs, rhs)


class TestMorphismArrow(MorphismTestCase):
    def test_arrow_identity(self):
        lhs, rhs = arrow_identity_expr(Morphism)
        self.assert_morphism_expr_equal(lhs, rhs)

    def test_arrow_composition(self):
        for f, g in fx_morphism.composition_pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrow_composition_expr(Morphism, f, g)
                self.assert_morphism_expr_equal(lhs, rhs)

    def test_arrow_first_identity(self):
        lhs, rhs = arrow_first_identity_expr(Morphism)
        self.assert_morphism_expr_equal(lhs, rhs, inputs=fx_morphism.pair_inputs())

    def test_arrow_first_composition(self):
        for f, g in fx_morphism.pairs():
            with self.subTest(f=f, g=g):
                lhs, rhs = arrow_first_composition_expr(Morphism, f, g)
                self.assert_morphism_expr_equal(lhs, rhs, inputs=fx_morphism.pair_inputs())

    def test_arrow_second(self):
        for value in fx_morphism.values():
            with self.subTest(value=value):
                lhs, rhs = arrow_second_expr(Morphism, value)
                self.assert_morphism_expr_equal(lhs, rhs, inputs=fx_morphism.pair_inputs())

    def test_arrow_split(self):
        for value1, value2 in fx_morphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrow_split_expr(Morphism, value1, value2)
                self.assert_morphism_expr_equal(lhs, rhs, inputs=fx_morphism.pair_inputs())

    def test_arrow_fanout(self):
        for value1, value2 in fx_morphism.pairs():
            with self.subTest(value1=value1, value2=value2):
                lhs, rhs = arrow_fanout_expr(Morphism, value1, value2)
                self.assert_morphism_expr_equal(lhs, rhs)
