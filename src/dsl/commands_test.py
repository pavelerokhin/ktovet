import unittest

from src.dsl.commands import *
from src.etc.driver import make_eager_driver


class TestsGetPageFindAllCommands(unittest.TestCase):
    def setUp(self):
        # Set up the Selenium WebDriver
        self.driver = make_eager_driver()

    def tearDown(self):
        # Quit the Selenium WebDriver
        self.driver.quit()

    def test_get_page(self):
        context = {
            "driver": self.driver,
            "url": "https://www.google.com/"
        }

        # Call the function
        get_page(context=context)

        # Assert that the page is loaded successfully
        self.assertEqual(self.driver.current_url, "https://www.google.com/")

    def test_find_all(self):
        context = {
            "driver": self.driver,
            "selector": "h1",
            "url": "https://www.google.com/",
            "timeout": 10,
        }

        # Navigate to a test page
        context = get_page(context=context)
        # Get search h1 elements
        context = find_all(context=context, result_to="elements")

        self.assertIsNotNone(context)
        elements = context.get("elements")
        self.assertIsNotNone(elements)
        # Assert that at least one element is found
        self.assertGreater(len(elements), 0)
        # Assert that the first element is a heading element
        self.assertEqual(elements[0].tag_name, "h1")


class TestExecuteJS(unittest.TestCase):
    def test_execute_js(self):
        context = {
            "driver": make_eager_driver(),
            "js": "console.log('Hello, World!');"
        }
        self.assertIsNotNone(execute_js(context=context))

    def test_execute_js_missing_context(self):
        with self.assertRaises(ValueError) as cm:
            execute_js(context={})
        self.assertIn(str(cm.exception), ["Missing driver in context", "Missing js in context"])

    def test_execute_js_missing_driver(self):
        context = {
            "js": "console.log('Hello, World!');"
        }
        with self.assertRaises(ValueError) as cm:
            execute_js(context=context)
        self.assertEqual(str(cm.exception), "Missing driver in context")

    def test_execute_js_missing_js(self):
        context = {
            "driver": make_eager_driver(),
        }
        with self.assertRaises(ValueError) as cm:
            execute_js(context=context)
        self.assertEqual(str(cm.exception), "Missing js in context")


class TestDriver(unittest.TestCase):
    def test_get_driver(self):
        context = eager_driver(context={})
        self.assertIsNotNone(context)


if __name__ == "__main__":
    unittest.main()
