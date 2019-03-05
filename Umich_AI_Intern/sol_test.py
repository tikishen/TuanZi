import unittest
from take_home import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_sum_digit(self):
        self.assertEqual(self.sol.sum_digit('abc'), '')
        self.assertEqual(self.sol.sum_digit('-'), '')
        self.assertEqual(self.sol.sum_digit('--'), '')
        self.assertEqual(self.sol.sum_digit('-a'), '')
        self.assertEqual(self.sol.sum_digit('aa-'), '')
        self.assertEqual(self.sol.sum_digit('1'), 1)
        self.assertEqual(self.sol.sum_digit('12'), 12)
        self.assertEqual(self.sol.sum_digit('12-'), 12)
        self.assertEqual(self.sol.sum_digit('12a'), 12)
        self.assertEqual(self.sol.sum_digit('12ab1'), 13)
        self.assertEqual(self.sol.sum_digit('-2'), -2)
        self.assertEqual(self.sol.sum_digit('--2'), -2)
        self.assertEqual(self.sol.sum_digit('---2-'), -2)
        self.assertEqual(self.sol.sum_digit('a-b1'), 1)
        self.assertEqual(self.sol.sum_digit('-2-2'), -4)
        self.assertEqual(self.sol.sum_digit('2-2'), 0)
        self.assertEqual(self.sol.sum_digit('2a-2'), 0)
        self.assertEqual(self.sol.sum_digit('0'), 0)
        self.assertEqual(self.sol.sum_digit('-0-'), 0)
        self.assertEqual(self.sol.sum_digit('--0'), 0)
        self.assertEqual(self.sol.sum_digit('2a-2+4'), 4)
        self.assertEqual(self.sol.sum_digit('12a34-5'), 41)


if __name__ == '__main__':
    unittest.main(verbosity=2)
