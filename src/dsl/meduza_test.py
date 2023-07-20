import unittest

from src.dsl.actions import Action, Actions
from src.dsl.commands.sln import find_all, get_attr, get_page
from src.etc.driver import make_eager_driver


class MeduzaTests(unittest.TestCase):
    def test_get_main_page_elements(self):
        context = {
            "driver": make_eager_driver(),
            "selector": "a.Link-root.Link-isInBlockTitle",
            "timeout": 10,
            "attr_text": "text",
            "attr_href": "href",
            "url": "https://meduza.io/",
        }

        # Define a mock schema with required attributes
        actions = Actions(actions=[Action(name="Get page", command=get_page),
                                   Action(name="Find all", command=find_all, result_to="elements"),
                                   Action(name="Get text", command=get_attr, input_mapping={"data": "elements", "attr": "attr_text"}, result_to="output_texts"),
                                   Action(name="Get hrefs", command=get_attr, input_mapping={"data": "elements", "attr": "attr_href"}, result_to="output_hrefs")],
                          context=context)

        context, fails = actions.do()

        # Assertions
        self.assertEqual(fails, [])
        self.assertIsNotNone(context.get("output_texts"))
        self.assertIsNotNone(context.get("output_hrefs"))
        self.assertEqual(len(context.get("output_texts")), len(context.get("output_hrefs")))
        self.assertEqual("a", context.get("elements")[0].tag_name)

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


class SeleniumAndDbCommandsTests(unittest.TestCase):
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
