import unittest

from Iterate import Iterate
from src.dsl.model.Action import Action
from src.dsl.model.Actions import Actions
from src.dsl.model.decorators import with_context


@with_context
def add_one(number):
    return number + 1


class TestIterate(unittest.TestCase):
    def test_do_with_no_iterator(self):
        actions = Actions(actions=[Action(
            name="add one",
            command=add_one,
            input_mapping={"number": "numbers"},
            result_to="number",
        )])  # Create an instance of the Actions class with your specific implementation
        context = {"numbers": [1, 2, 3]}
        iterate_obj = Iterate(actions=actions, context=context, iterator="")

        with self.assertRaises(ValueError) as context_manager:
            iterate_obj.do()

        self.assertEqual(str(context_manager.exception), "Nothing to iterate")

    def test_do(self):
        actions = Actions(actions=[Action(
            name="add one",
            command=add_one,
            input_mapping={"number": "numbers"},
            result_to="out",
        )])  # Create an instance of the Actions class with your specific implementation
        context = {"numbers": [1, 2, 3]}
        iterator = "numbers"
        iterate_obj = Iterate(actions, iterator, context)

        ctx, failure = iterate_obj.do()
        self.assertEqual(failure, [])
        self.assertEqual(ctx.get("out"), [2, 3, 4])

    def test_do_with_elements(self):
        # Replace this with your specific implementation of the Actions class
        class MockActions(Actions):
            def do(self, context):
                # Mock implementation of the 'do' method for testing purposes
                new_context = context.copy()
                new_context["result"] = context["number"] * 2
                return new_context, []

        actions = MockActions()
        context = {"number": [1, 2, 3]}
        iterator = "number"
        iterate_obj = Iterate(actions, iterator, context)

        result, _ = iterate_obj.do()

        # Verify that the 'result' key is updated correctly in the context
        self.assertEqual(result, {"number": 3, "result": 6})

        # Verify that only the 'result' key is updated in the context
        self.assertEqual(len(result), 2)
        self.assertIn("number", result)
        self.assertIn("result", result)


if __name__ == '__main__':
    unittest.main()