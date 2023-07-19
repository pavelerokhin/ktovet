import inspect
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.etc.driver import make_eager_driver


def context_wrapper(func):
    def wrapper(**kwargs):
        if kwargs.keys() != {"context"}:
            raise Exception("Invalid arguments")
        context = kwargs.get("context")  # should always have context
        if context is None:
            raise Exception("Missing context")

        context = dict(context)
        params = {}
        func_signature = inspect.signature(func)
        for param_name, param in func_signature.parameters.items():
            if param_name not in context.keys():
                raise Exception(f"Missing {param_name} in context, func {func.__name__}")
            params = {param_name: context[param_name]}

        result = func(**params)
        context[f"result_{func.__name__}"] = result

        return context

    return wrapper


@context_wrapper
def execute_js(driver, js):
    driver.execute_script(js)


@context_wrapper
def driver():
    return make_eager_driver()


@context_wrapper
def find_all(driver, timeout, selector):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )

    return elements


@context_wrapper
def get_page(driver, url):
    driver.get(url)


@context_wrapper
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
