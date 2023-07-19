import unittest

# Import the functions you want to test here
from decorators import function, function_with_result


class TestFunctionDecorator(unittest.TestCase):

    # Test cases for function decorator

    def test_function_with_valid_context(self):
        @function
        def my_function(a, b):
            return a + b

        context = {"a": 5, "b": 10}
        result = my_function(context=context)

        self.assertEqual(result, context)

    def test_function_missing_context(self):
        @function
        def my_function(a, b):
            return a + b

        with self.assertRaises(ValueError):
            my_function()

    def test_function_invalid_argument(self):
        @function
        def my_function(a, b):
            return a + b

        with self.assertRaises(ValueError):
            my_function(c={"a": 5, "b": 10})

    def test_function_missing_parameter(self):
        @function
        def my_function(a, b):
            return a + b

        with self.assertRaises(ValueError):
            my_function(context={"a": 5})

    # Test cases for function_with_result decorator

    def test_function_with_result_valid_context(self):
        @function_with_result
        def multiply(a, b):
            return a * b

        context = {"a": 5, "b": 10}
        result = multiply(context=context, result_to="result")

        self.assertEqual(result, {"a": 5, "b": 10, "result": 50})

    def test_function_with_result_missing_context(self):
        @function_with_result
        def multiply(a, b):
            return a * b

        with self.assertRaises(ValueError):
            multiply(result_to="result")

    def test_function_with_result_missing_result_to(self):
        @function_with_result
        def multiply(a, b):
            return a * b

        with self.assertRaises(ValueError):
            multiply(context={"a": 5, "b": 10})


if __name__ == "__main__":
    unittest.main()
