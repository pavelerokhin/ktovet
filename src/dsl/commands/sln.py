import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.dsl.model.decorators import with_context
from src.etc.driver import make_eager_driver


@with_context
def execute_js(driver, js):
    driver.execute_script(js)


@with_context
def eager_driver():
    return make_eager_driver()


@with_context
def find_all(driver, timeout, selector):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )

    return elements


@with_context
def get_attr(data, attr):
    out = []
    for element in data:
        v = element.get_attribute(attr)
        if v:
            out.append(v)
        else:
            out.append(None)

    return out


@with_context
def get_page(driver, url):
    driver.get(url)


@with_context
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
