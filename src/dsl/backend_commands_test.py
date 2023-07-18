import unittest

from backend.stage import Stage
from backend.actions import Action, Actions
from commands.sel import find_all, get_page
from src.etc.driver import make_eager_driver


class BackendCommandsTests(unittest.TestCase):
    def test_find_elements(self):
        context = {
            "driver": make_eager_driver(),
            "selector": "h1",
            "url": "https://www.google.com",
        }

        # Define a mock schema with required attributes
        schema = {
            "id": "Get two google buttons",
            "actions":  Actions([
                Action(name="Simple Action", command=get_page, context=context),
                Action(name="Find button", command=find_all, context=context)
            ])
        }

        s = Stage(schema)
        elements, fails = s.do()

        # Assertions
        self.assertEqual(fails, [])
        self.assertEqual(1, len(elements))
        self.assertEqual("h1", elements[0].tag_name)

    def test_stage_failure(self):
        context = {
            "driver": make_eager_driver(),
            "url": "asfasdfasfasfasdfscfvbdfvbsdfgwfasdg.zzz",
        }

        # Define a mock schema with required attributes
        schema = {
            "id": "Get noy existent site",
            "actions":  Actions([Action(name="load site", command=get_page, context=context)])
        }

        s = Stage(schema)
        result, fails = s.do()

        # Assertions
        self.assertNotEqual(fails,  [])


if __name__ == '__main__':
    unittest.main()
