import unittest
from lib.scorer import Scorer


class TestScorer(unittest.TestCase):
    def test_bm25(self):
        s = Scorer(['With', 'longer', 'battery', 'life', 'upgraded', 'storage', 'camera', 'updates', 'and', 'the', 'new', 'A15', 'Bionic', 'processor', 'Apple', "'s", 'iPhone', '13', 'is', 'tempting', 'choice', 'when', 'picking', 'new', 'iPhone', 'Check', 'out', 'some', 'of', 'the', 'best', 'iPhone', 'deals', 'here', 'But', 'depending', 'on', 'your', 'personal',
                   'budget', 'and', 'smartphone', 'needs', 'you', 'may', 'want', 'to', 'consider', 'other', 'options', 'like', 'the', 'iPhone', '12', 'iPhone', '11', 'or', 'iPhone', 'SE', 'You', 'could', 'wait', 'for', 'the', 'iPhone', '14', 'or', 'iPhone', 'SE', 'too', 'With', 'that', 'in', 'mind', 'does', 'it', 'make', 'sense', 'to', 'buy', 'an', 'iPhone', '12', 'in', '2021'])

        res = s.bm25()
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 66)


if __name__ == "__main__":
    unittest.main()
