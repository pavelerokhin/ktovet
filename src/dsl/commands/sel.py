import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def execute_js(context=None):
    if context is None or "driver" not in context or "js" not in context:
        raise Exception("Invalid context or missing driver or js")

    driver = context["driver"]
    js = context["js"]
    driver.execute_script(js)


def find_all(context=None, timeout=10):
    if context is None or "driver" not in context or "selector" not in context:
        raise Exception("Invalid context or missing driver or selector")

    driver = context["driver"]
    selector = context["selector"]

    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
    return elements


def get_page(context=None):
    if context is None or "driver" not in context or "url" not in context:
        raise Exception("Invalid context or missing driver or url")

    driver = context["driver"]
    url = context["url"]
    driver.get(url)


def download_csv(context=None):
    if context is None or "download_path" not in context:
        raise Exception("Invalid context or missing download_path")

    download_path = context["download_path"]

    # Wait until the file loads
    timeout = 5
    time_elapsed = 0
    time_step = 0.5

    while True:
        if any(file_name.endswith('.csv') for file_name in os.listdir(download_path)):
            break

        time.sleep(time_step)
        time_elapsed += time_step

        if time_elapsed > timeout:
            if len(os.listdir(download_path)) == 0:
                raise TimeoutError("Timeout, no files in directory")
            else:
                raise TimeoutError("Timeout")
