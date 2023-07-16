import unittest

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from src.etc.driver import default_options, make_eager_driver, make_eager_driver_no_js


class SeleniumTests(unittest.TestCase):

    def test_default_options(self):
        # Test case 1: Download path is None
        chrome_options1 = Options()
        download_path1 = None

        default_options(chrome_options1, download_path1)

        # Assert that the prefs are set correctly for download_path=None
        prefs1 = chrome_options1.experimental_options["prefs"]
        self.assertFalse("download.default_directory" in prefs1)
        self.assertTrue("download.prompt_for_download" in prefs1)
        self.assertTrue("download.directory_upgrade" in prefs1)

        # Test case 2: Download path is not None
        chrome_options2 = Options()
        download_path2 = "/path/to/downloads"

        default_options(chrome_options2, download_path2)

        # Assert that the prefs are set correctly for download_path=/path/to/downloads
        prefs2 = chrome_options2.experimental_options["prefs"]
        self.assertEqual(prefs2["download.default_directory"], download_path2)
        self.assertTrue("download.prompt_for_download" in prefs2)
        self.assertTrue("download.directory_upgrade" in prefs2)

    def test_make_eager_driver(self):
        # Test case 1: Download path is None
        download_path1 = None

        driver1 = make_eager_driver(download_path1)

        # Assert that the driver is an instance of WebDriver
        self.assertIsInstance(driver1, WebDriver)

        # Test case 2: Download path is not None
        download_path2 = "/path/to/downloads"

        driver2 = make_eager_driver(download_path2)

        # Assert that the driver is an instance of WebDriver
        self.assertIsInstance(driver2, WebDriver)

    def test_make_eager_driver_no_js(self):
        # Test case 1: Download path is None
        download_path1 = None

        driver1 = make_eager_driver_no_js(download_path1)

        # Assert that the driver is an instance of WebDriver
        self.assertIsInstance(driver1, WebDriver)

        # Test case 2: Download path is not None
        download_path2 = "/path/to/downloads"

        driver2 = make_eager_driver_no_js(download_path2)

        # Assert that the driver is an instance of WebDriver
        self.assertIsInstance(driver2, WebDriver)


if __name__ == "__main__":
    unittest.main()
