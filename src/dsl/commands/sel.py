import os
import time

from selenium.webdriver.common.by import By


def find_all(context=None):
    if context is None or "driver" not in context or "selector" not in context:
        raise Exception("Invalid context or missing driver or selector")

    driver = context["driver"]
    selector = context["selector"]
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
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