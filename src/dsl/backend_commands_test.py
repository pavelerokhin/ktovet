import unittest

from backend.stage import stage
from backend.action import Action, Actions
from commands.sel import find_all, get_page
from src.etc.driver import make_eager_driver


class BackendCommandsTests(unittest.TestCase):
    def test_find_elements(self):
        context = {
            "driver": make_eager_driver(),
            "selector": "input[value='Google Search']",
            "url": "https://www.google.com",
        }

        # Define a mock schema with required attributes
        schema = {
            "id": "Get two google buttons",
            "actions":  Actions([
                Action(name="Simple Action", func=get_page, context=context),
                Action(name="Find button", func=find_all, context=context)
            ])
        }

        elements, fails = stage(schema)

        # Assertions
        self.assertEqual(fails, [])
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0].tag_name, "input")

    def test_stage_failure(self):
        context = {
            "driver": make_eager_driver(),
            "url": "asfasdfasfasfasdfscfvbdfvbsdfgwfasdg.zzz",
        }

        # Define a mock schema with required attributes
        schema = {
            "id": "Get noy existent site",
            "actions":  Actions([Action(name="load site", func=get_page, context=context)])
        }

        result, fails = stage(schema)

        # Assertions
        self.assertNotEqual(fails,  [])


if __name__ == '__main__':
    unittest.main()
