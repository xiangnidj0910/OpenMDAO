from openmdao.api import OptionsDictionary
import unittest
from six import PY3, assertRegex


class TestOptionsDict(unittest.TestCase):

    def setUp(self):
        self.dict = OptionsDictionary()

    def test_type_checking(self):
        self.dict.declare('test', type_=int, desc='Test integer value')

        self.dict['test'] = 1
        self.assertEqual(self.dict['test'], 1)

        with self.assertRaises(TypeError) as context:
            self.dict['test'] = ''

        class_or_type = 'class' if PY3 else 'type'
        expected_msg = "Entry 'test' has the wrong type (<{} 'int'>)".format(class_or_type)
        self.assertEqual(expected_msg, str(context.exception))

        # make sure bools work
        self.dict.declare('flag', default=False, type_=bool)
        self.assertEqual(self.dict['flag'], False)
        self.dict['flag'] = True
        self.assertEqual(self.dict['flag'], True)

    def test_type_and_values(self):
        # Test with only type_
        self.dict.declare('test1', type_=int)
        self.dict['test1'] = 1
        self.assertEqual(self.dict['test1'], 1)

        # Test with only values
        self.dict.declare('test2', values=['a', 'b'])
        self.dict['test2'] = 'a'
        self.assertEqual(self.dict['test2'], 'a')

        # Test with both type_ and values
        self.dict.declare('test3', type_=int, values=['a', 'b'])
        self.dict['test3'] = 1
        self.assertEqual(self.dict['test3'], 1)
        self.dict['test3'] = 'a'
        self.assertEqual(self.dict['test3'], 'a')

    def test_isvalid(self):
        self.dict.declare('even_test', type_=int, is_valid=lambda x: x%2 == 0)
        self.dict['even_test'] = 2
        self.dict['even_test'] = 4

        with self.assertRaises(ValueError) as context:
            self.dict['even_test'] = 3

        expected_msg = "Function is_valid returns False for {}.".format('even_test')
        self.assertEqual(expected_msg, str(context.exception))

    def test_unnamed_args(self):
        with self.assertRaises(KeyError) as context:
            self.dict['test'] = 1

        # KeyError ends up with an extra set of quotes.
        expected_msg = "\"Key 'test' cannot be set because it has not been declared.\""
        self.assertEqual(expected_msg, str(context.exception))

    def test_contains(self):
        self.dict.declare('test')

        contains = 'undeclared' in self.dict
        self.assertTrue(not contains)

        contains = 'test' in self.dict
        self.assertTrue(contains)

    def test_update(self):
        self.dict.declare('test', default='Test value', type_=object)

        obj = object()
        self.dict.update({'test': obj})
        self.assertIs(self.dict['test'], obj)

    def test_update_extra(self):
        with self.assertRaises(KeyError) as context:
            self.dict.update({'test': 2})

        # KeyError ends up with an extra set of quotes.
        expected_msg = "\"Key 'test' cannot be set because it has not been declared.\""
        self.assertEqual(expected_msg, str(context.exception))

    def test_get_missing(self):
        with self.assertRaises(KeyError) as context:
            self.dict['missing']

        expected_msg = "\"Entry 'missing' cannot be found\""
        self.assertEqual(expected_msg, str(context.exception))

    def test_get_default(self):
        obj_def = object()
        obj_new = object()

        self.dict.declare('test', default=obj_def, type_=object)

        self.assertIs(self.dict['test'], obj_def)

        self.dict['test'] = obj_new
        self.assertIs(self.dict['test'], obj_new)

    def test_values(self):
        obj1 = object()
        obj2 = object()
        self.dict.declare('test', values=[obj1, obj2])

        self.dict['test'] = obj1
        self.assertIs(self.dict['test'], obj1)

        with self.assertRaises(ValueError) as context:
            self.dict['test'] = object()

        expected_msg = ("Entry 'test''s value is not one of \[<object object at 0x[0-9A-Fa-f]+>,"
                        " <object object at 0x[0-9A-Fa-f]+>\]")
        assertRegex(self, str(context.exception), expected_msg)

    def test_read_only(self):
        opt = OptionsDictionary(read_only=True)
        opt.declare('permanent', 3.0)

        with self.assertRaises(KeyError) as context:
            opt['permanent'] = 4.0

        expected_msg = ("Tried to set 'permanent' on a read-only OptionsDictionary")
        assertRegex(self, str(context.exception), expected_msg)

    def test_bounds(self):
        self.dict.declare('x', default=1.0, lower=0.0, upper=2.0)

        with self.assertRaises(ValueError) as context:
            self.dict['x'] = 3.0

        expected_msg = ("Value of 3.0 exceeds maximum of 2.0 for entry 'x'")
        assertRegex(self, str(context.exception), expected_msg)

        with self.assertRaises(ValueError) as context:
            self.dict['x'] = -3.0

        expected_msg = ("Value of -3.0 exceeds minimum of 0.0 for entry 'x'")
        assertRegex(self, str(context.exception), expected_msg)


if __name__ == "__main__":
    unittest.main()
