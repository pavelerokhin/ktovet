import unittest

from src.dsl.actions import Action, Actions
from src.dsl.commands.sln import find_all, get_page
from src.etc.driver import make_eager_driver


class BackendCommandsTests(unittest.TestCase):
    def test_find_elements(self):
        context = {
            "driver": make_eager_driver(),
            "selector": "body",
            "timeout": 10,
            "url": "https://www.google.com",
        }

        # Define a mock schema with required attributes
        actions = Actions(actions=[Action(name="Get page", command=get_page),
                                   Action(name="Find all", command=find_all, result_to="elements")],
                          context=context)

        context, fails = actions.do()

        # Assertions
        self.assertEqual(fails, [])
        self.assertAlmostEqual(1, len(context.get("elements")))
        self.assertEqual("body", context.get("elements")[0].tag_name)

    def test_stage_failure(self):
        context = {
            "driver": make_eager_driver(),
            "url": "asfasdfasfasfasdfscfvbdfvbsdfgwfasdg.zzz",
        }

        # Define a mock schema with required attributes
        actions = Actions(actions=[Action(name="load site", command=get_page)],
                          context=context)

        result, fails = actions.do()

        # Assertions
        self.assertNotEqual(fails,  [])


if __name__ == '__main__':
    unittest.main()
