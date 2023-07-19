import unittest

from actions import Action, Actions


class ActionTests(unittest.TestCase):
    def test_action_with_required_args(self):
        def my_func(context=None):
            return context

        action = Action("Test Action", my_func)
        action.do({"text": "xxx"})
        self.assertEqual(action.context, {"text": "xxx"})

    def test_action_missing_required_args(self):
        def my_func(context):
            if context is None:
                raise ValueError("Invalid context or missing text")

            return context

        with self.assertRaises(ValueError):
            Action("Test Action", my_func).do(None)

    def test_actions_execution(self):
        def add_one(context):
            if context is None or "data" not in context:
                raise Exception("Invalid context or missing data")

            data = context["data"]
            context["data"] = data + 1

            return context

        def multiply_by_two(context):
            if context is None or "data" not in context:
                raise Exception("Invalid context or missing data")

            data = context["data"]
            context["data"] = data * 2

            return context

        context = {"data": 0}
        actions = [Action("Add One", add_one), Action("Multiply by Two", multiply_by_two)]
        context, fails = Actions(actions, context, to_store=["data"]).do()
        self.assertEqual([], fails)
        self.assertEqual(2, context["data"])


if __name__ == '__main__':
    unittest.main()
