import unittest
from typeclass.data.maybe import Maybe, Just, Nothing

class TestMaybe(unittest.TestCase):

    def test_fmap(self):
        self.assertEqual(Just(1).fmap(lambda x: x + 2), Just(3))
        self.assertEqual(Nothing().fmap(lambda x: x + 2), Nothing())

    def test_ap(self):
        self.assertEqual(Just(lambda x: x + 1).ap(Just(3)), Just(4))
        self.assertEqual(Nothing().ap(Just(3)), Nothing())
        self.assertEqual(Just(lambda x: x + 1).ap(Nothing()), Nothing())

    def test_pure(self):
        self.assertEqual(Maybe.pure(10), Just(10))

    def test_symbolic_syntax(self):
        from typeclass.syntax.symbols import fmap, ap, pure
        self.assertEqual((Just(10) |fmap| (lambda x: x * 2)), Just(20))
        self.assertEqual((Maybe |pure| (lambda x: lambda y: x + y) |ap| Just(1) |ap| Just(2)), Just(3))

