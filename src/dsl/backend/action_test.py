import unittest

from actions import Action, Actions


class ActionTests(unittest.TestCase):
    def test_action_with_required_args(self):
        def my_func(data=None, context=None):
            return data, context

        action = Action("Test Action", my_func)
        result = action.do(data="test data", context="test context")
        self.assertEqual(result, ("test data", "test context"))

    def test_action_missing_required_args(self):
        def my_func(data=None):
            return data

        with self.assertRaises(ValueError):
            action = Action("Test Action", my_func)

    def test_actions_execution(self):
        def add_one(data=0, context=None):
            return data + 1, None

        def multiply_by_two(data=0, context=None):
            return data * 2, None

        actions = [Action("Add One", add_one), Action("Multiply by Two", multiply_by_two)]
        actions_obj = Actions(actions)
        result = actions_obj.do(data=1, context=None)
        self.assertEqual(result, (4, []))


if __name__ == '__main__':
    unittest.main()
