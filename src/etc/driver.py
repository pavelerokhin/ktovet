from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ban_list = ["https://stats.oecd.org/ViewHTML.aspx",
            "https://script.crazyegg.com",
            "https://region1.google-analytics.com",
            "https://www.oecd-ilibrary.org",
            "https://www.google.com/ads/"]


def default_options(chrome_options, download_path):
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    })

    chrome_options.page_load_strategy = 'eager'

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")


def make_eager_driver(download_path):
    chrome_options = Options()
    default_options(chrome_options, download_path)

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def make_eager_driver_no_js(download_path):
    chrome_options = Options()
    default_options(chrome_options, download_path)

    chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def make_eager_driver_no_aspx(download_path):
    driver = make_eager_driver(download_path)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ban_list})
    driver.execute_cdp_cmd('Network.enable', {})

    return driver


def make_eager_driver_no_aspx_no_js(download_path=None):
    driver = make_eager_driver_no_js(download_path)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ban_list})
    driver.execute_cdp_cmd('Network.enable', {})

    return driver
