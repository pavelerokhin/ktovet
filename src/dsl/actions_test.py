import unittest

from src.dsl.model.Action import Action
from src.dsl.model.Actions import Actions
from src.dsl.commands.sln import with_context


class ActionTests(unittest.TestCase):
    def test_action_with_required_args(self):
        @with_context
        def my_func(text):
            return text + " test"

        action = Action(name="Test Action", command=my_func, result_to="result")
        context = action.do({"text": "xxx"})

        self.assertIsNotNone(context)
        self.assertIsNotNone(context.get("result"))
        self.assertEqual(context.get("result"), "xxx test")

    def test_action_missing_required_args(self):
        @with_context
        def my_func():
            return "test"

        with self.assertRaises(ValueError):
            Action("Test Action", my_func).do(None)

    def test_actions_execution(self):
        @with_context
        def add_one(data):
            return data + 1

        @with_context
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
