import unittest

from actions import Action, Actions
from src.dsl.commands.sln import function, function_with_result


class ActionTests(unittest.TestCase):
    def test_action_with_required_args(self):
        @function_with_result
        def my_func(text):
            return text + " test"

        action = Action(name="Test Action", command=my_func, result_to="result")
        context = action.do({"text": "xxx"})

        self.assertIsNotNone(context)
        self.assertIsNotNone(context.get("result"))
        self.assertEqual(context.get("result"), "xxx test")

    def test_action_missing_required_args(self):
        @function
        def my_func():
            return "test"

        with self.assertRaises(ValueError):
            Action("Test Action", my_func).do(None)

    def test_actions_execution(self):
        @function_with_result
        def add_one(data):
            return data + 1

        @function_with_result
        def multiply_by_two(data):
            return data * 2

        context = {"data": 0}
        actions = [Action(name="Add One", command=add_one, result_to="data"),
                   Action(name="Multiply by Two", command=multiply_by_two, result_to="data")]
        context, fails = Actions(actions, context).do()
        self.assertEqual([], fails)
        self.assertEqual(2, context["data"])


if __name__ == '__main__':
    unittest.main()
