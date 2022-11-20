import unittest
from unittest.mock import patch

import abc


class ABClass(abc.ABC):
    def concrete_method(self):
        return 'something'

    @abc.abstractmethod
    def abstract_method(self):
        pass

    def concrete_method_that_uses_abstract_method(self):
        return 'value1 plus '+self.abstract_method()


class TestABClassMuteAbstractMethods(unittest.TestCase):
    @patch.multiple(ABClass, __abstractmethods__=set())
    def test_mock_all_abstract_methods(self):
        self.assertEqual(ABClass().concrete_method(), 'something')


class TestABClassMakeConcreteClass(unittest.TestCase):
    class ConcreteClass(ABClass):
        def abstract_method(self):
            pass

    def test_concrete_methods(self):
        self.assertEqual(TestABClassMakeConcreteClass.ConcreteClass().concrete_method(), 'something')


class TestABCClassPatchABCMethod(unittest.TestCase):
    @patch.object(ABClass, 'abstract_method', return_value='value2')
    def test_concrete_method_that_uses_abstract_method(self, *mock_arg):
        ABClass.__abstractmethods__ = set()
        obj = ABClass()
        self.assertEqual(obj.concrete_method_that_uses_abstract_method(), 'value1 plus value2')



if __name__ == '__main__':
    unittest.main()
