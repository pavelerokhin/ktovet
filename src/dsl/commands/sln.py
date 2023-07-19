import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.dsl.decorators import function, function_with_result
from src.etc.driver import make_eager_driver


@function
def execute_js(driver, js):
    driver.execute_script(js)


@function
def eager_driver():
    return make_eager_driver()


@function_with_result
def find_all(driver, timeout, selector):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )

    return elements


@function
def get_page(driver, url):
    driver.get(url)


@function_with_result
def download_csv(download_path, timeout):
    # Wait until the file loads
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
