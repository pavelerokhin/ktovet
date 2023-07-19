import unittest

from src.dsl.commands.sel import *
from src.etc.driver import make_eager_driver


class SeleniumTests(unittest.TestCase):
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
        get_page(context)

        # Assert that the page is loaded successfully
        self.assertEqual(self.driver.current_url, "https://www.google.com/")

    def test_find_all(self):
        context = {
            "driver": self.driver,
            "selector": "h1",
            "url": "https://www.google.com/"
        }

        # Navigate to a test page
        context = get_page(context)
        # Get search button elements
        elements = find_all(context)["find_all_result"]

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
        self.assertIsNotNone(execute_js(context))

    def test_execute_js_missing_context(self):
        with self.assertRaises(Exception) as cm:
            execute_js()
        self.assertEqual(str(cm.exception), "Invalid context or missing driver or js")

    def test_execute_js_missing_driver(self):
        context = {
            "js": "console.log('Hello, World!');"
        }
        with self.assertRaises(Exception) as cm:
            execute_js(context)
        self.assertEqual(str(cm.exception), "Invalid context or missing driver or js")

    def test_execute_js_missing_js(self):
        context = {
            "driver": make_eager_driver(),
        }
        with self.assertRaises(Exception) as cm:
            execute_js(context)
        self.assertEqual(str(cm.exception), "Invalid context or missing driver or js")


class TestDriver(unittest.TestCase):
    def test_get_driver(self):
        context = driver(context={})
        self.assertIsNotNone(context.get("result_driver"))


if __name__ == "__main__":
    unittest.main()
