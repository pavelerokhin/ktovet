import unittest

from src.dsl.commands.sel import get_page, find_all
from src.etc.driver import make_eager_driver


class SeleniumTests(unittest.TestCase):
    def setUp(self):
        # Set up the Selenium WebDriver
        self.driver = make_eager_driver(None)

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
            "selector": "input[value='Google Search']",
            "url": "https://www.google.com/"
        }

        # Navigate to a test page
        get_page(context)
        # Get search button elements
        elements = find_all(context)

        # Assert that at least one element is found
        self.assertGreater(len(elements), 0)
        # Assert that the first element is a heading element
        self.assertEqual(elements[0].tag_name, "input")



if __name__ == "__main__":
    unittest.main()
