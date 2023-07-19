import inspect
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.etc.driver import make_eager_driver


def context_to_params(context, func):
    context = dict(context)
    params = {}
    func_signature = inspect.signature(func)
    for param_name, _ in func_signature.parameters.items():
        if param_name not in context.keys():
            raise ValueError(f"Missing {param_name} in context")
        params[param_name] = context[param_name]

    return params


def function(func):
    def wrapper(**kwargs):
        if "context" not in kwargs.keys():
            raise ValueError("Invalid arguments")

        context = kwargs.get("context")  # should always have context
        if context is None:
            raise ValueError("Missing context")

        params = context_to_params(context, func)

        func(**params)  # call the function and ignore the return value

        return context

    return wrapper


def function_with_result(func):
    def wrapper(**kwargs):
        if "context" not in kwargs.keys() and "result_to" not in kwargs.keys():
            raise ValueError("Invalid arguments")

        context = kwargs.get("context")  # should always have context
        if context is None:
            raise ValueError("Missing context")
        result_to = kwargs.get("result_to")  # should always have context
        if result_to is None:
            raise ValueError("Missing result_to")

        params = context_to_params(context, func)

        result = func(**params)
        context[result_to] = result

        return context

    return wrapper


@function
def execute_js(driver, js):
    driver.execute_script(js)


@function
def driver():
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
