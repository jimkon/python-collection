import unittest
from unittest.mock import patch


class Object:
    def __init__(self):
        self.value = 'value_BEFORE_change_value_is_called'
        self.change_value_method()

        self.return_value = 'ORIGINAL_return_value'

    def change_value_method(self):
        self.value = 'value_AFTER_change_value_is_called'

    def return_value_method(self):
        return self.return_value

    def another_method(self):
        return 'value'


class TestMockMethod(unittest.TestCase):
    def test_mock_to_mute(self):
        # Before muting
        self.assertEqual(Object().value, 'value_AFTER_change_value_is_called')

        # After muting
        with patch.object(Object, 'change_value_method'):
            self.assertEqual(Object().value, 'value_BEFORE_change_value_is_called')

    def test_mock_to_change_return_value(self):
        # Before mocking
        self.assertEqual(Object().return_value_method(), 'ORIGINAL_return_value')

        # After mocking
        with patch.object(Object, 'return_value_method', return_value='MOCKED_return_value'):
            self.assertEqual(Object().return_value_method(), 'MOCKED_return_value')

    @patch.object(Object, 'change_value_method', side_effect=Exception)
    def test_mock_exception_raising(self, mock_change_value_method):
        with self.assertRaises(Exception):
            Object().change_value_method()

    @patch.object(Object, 'change_value_method')
    @patch.object(Object, 'return_value_method')
    @patch.object(Object, 'another_method')
    def test_mock_multiple_methods(self, mock_ANOTHER_method, mock_RETURN_VALUE_method, mock_CHANGE_VALUE_method):
        """ CAREFUL with THE ORDER of the args """
        assert True

    @patch.object(Object, '__init__', return_value=None) # important to return None from __init__
    def test_init_method(self, mock_init):
        Object()
        mock_init.assert_called_once()


if __name__ == '__main__':
    unittest.main()