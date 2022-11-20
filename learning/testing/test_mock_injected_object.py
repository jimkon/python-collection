import unittest
from unittest.mock import MagicMock


class InjectedObjectClass:
    def function(self):
        pass

    def return_function(self):
        return 'original_return'


class AClass:
    def __init__(self, injected_object):
        self.injected_object = injected_object

    def do_something(self):
        self.injected_object.function()
        return self.injected_object.return_function()


class TestTheClass(unittest.TestCase):
    def test_do_something(self):
        mock_inj_object = MagicMock()
        mock_inj_object.function = MagicMock()
        mock_inj_object.return_function = MagicMock(return_value='mocked_return')

        obj = AClass(mock_inj_object)
        self.assertIsNotNone(obj.injected_object)
        self.assertEqual(obj.do_something(), 'mocked_return')


if __name__ == '__main__':
    unittest.main()
