import unittest
import stage

from action import Action, Actions


class StageTestCase(unittest.TestCase):
    def simple_action(self, data=None, context=None):
        return data, []

    def test_stage_success(self):
        # Define a mock schema with required attributes
        schema = {
            "id": "Simple Schema",
            "actions":  Actions([Action("Simple Action", self.simple_action)])
        }

        data = [4, 5, 6]
        result = stage.stage(data, schema)

        # Assertions
        self.assertEqual(result, ([4, 5, 6], []))

    def test_stage_failure(self):
        # Define a mock schema with required attributes
        schema = {
            "id": "Simple Schema",
            "actions":  Actions([Action("Simple Action", self.simple_action)])
        }

        data = [4, 5, 6]
        result = stage.stage(data, schema)

        # Assertions
        self.assertNotEqual(result,  ([7, 8, 9], []))

    def test_stage_invalid_schema(self):
        data = [1, 2, 3]

        # Assertions
        with self.assertRaises(ValueError):
            stage.stage(data)


if __name__ == '__main__':
    unittest.main()
