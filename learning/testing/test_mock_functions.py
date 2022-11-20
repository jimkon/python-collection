import unittest
from unittest.mock import patch, call


class Obj:
    def function_pow(self, n):
        return n**2

    def function_first_n_pows(self, n):
        return [self.function_pow(v) for v in range(n)]


class TestFunctions(unittest.TestCase):
    def test_function_first_n_pows(self):
        self.assertListEqual(Obj().function_first_n_pows(4), [0, 1, 4, 9])

    @patch.object(Obj, 'function_pow', return_value=3)
    def test_function_first_n_pows_mock_pow(self, mock_pow):
        self.assertListEqual(Obj().function_first_n_pows(4), [3, 3, 3, 3])
        self.assertEqual(mock_pow.call_count, 4)
        mock_pow.assert_has_calls([call(0), call(1), call(2), call(3)])

    @patch.object(Obj, 'function_pow', side_effect=lambda x: x*2)
    def test_function_first_n_pows_mock_pow_func(self, mock_pow):
        self.assertListEqual(Obj().function_first_n_pows(4), [0, 2, 4, 6])

    @patch.object(Obj, 'function_pow', side_effect=[5, 7, 11, 0])
    def test_function_first_n_pows_mock_pow_iter(self, mock_pow):
        self.assertListEqual(Obj().function_first_n_pows(4), [5, 7, 11, 0])


if __name__ == '__main__':
    unittest.main()
