import unittest

# Import the functions you want to test here
from decorators import sln


class TestFunctionDecorator(unittest.TestCase):

    # Test cases for function decorator

    def test_function_with_valid_context(self):
        @sln
        def my_function(a, b):
            return a + b

        context = {"a": 5, "b": 10}
        result = my_function(context=context)

        self.assertEqual(result, context)

    def test_function_missing_context(self):
        @sln
        def my_function(a, b):
            return a + b

        with self.assertRaises(ValueError):
            my_function()

    def test_function_invalid_argument(self):
        @sln
        def my_function(a, b):
            return a + b

        with self.assertRaises(ValueError):
            my_function(c={"a": 5, "b": 10})

    def test_function_missing_parameter(self):
        @sln
        def my_function(a, b):
            return a + b

        with self.assertRaises(ValueError):
            my_function(context={"a": 5})

    # Test cases for function_with_result decorator

    def test_function_with_result_valid_context(self):
        @sln
        def multiply(a, b):
            return a * b

        context = {"a": 5, "b": 10}
        result = multiply(context=context, result_to="result")

        self.assertEqual(result, {"a": 5, "b": 10, "result": 50})

    def test_function_with_result_missing_context(self):
        @sln
        def multiply(a, b):
            return a * b

        with self.assertRaises(ValueError):
            multiply(result_to="result")


if __name__ == "__main__":
    unittest.main()
