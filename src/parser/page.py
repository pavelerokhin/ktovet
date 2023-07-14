import os
import time

from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..etc.parallel import save_in_parallel
from ..etc.driver import make_eager_driver_no_aspx
from ..etc.utils import GREEN, HEADER, RED, remove_directory, WHITE


REDIRECT_TO_SURVEY_CSV = "redirectToSurvey('csv')"


def get_page(driver, url, error_type):
    driver.get(url)


def crawl_page(driver):
    pass


def download_csv(download_path, error_type):
    # wait until the file loads
    timeout = 5
    time_elapsed = 0
    time_step = 0.5

    if error_type == "TimeoutError":
        timeout = 120

    while not any(file_name.endswith('.csv') for file_name in os.listdir(download_path)):
        time.sleep(time_step)
        time_elapsed += time_step

        if time_elapsed > timeout:
            if len(os.listdir(download_path)) == 0:
                raise TimeoutError("Timeout, no files in directory")
            raise TimeoutError("Timeout")


def process_routine(page, t0, out, fails, download_path):
    driver = make_eager_driver_no_aspx(download_path)

    try:
        get_page(driver, None, None)
        crawl_page(driver)

    except NoSuchElementException as e:
        print(f"* {RED}FAIL{WHITE} {HEADER}Element not found{WHITE} {round(time.time() - t0, 2)}s")
        page['error'] = type(e).__name__
        fails.append(page)
        remove_directory(download_path)
    except TimeoutError as e:
        print(f"[* {RED}FAIL{WHITE} {HEADER}Timeout{WHITE} {round(time.time() - t0, 2)}s")
        page['error'] = type(e).__name__
        fails.append(page)
        remove_directory(download_path)
    except JavascriptException as e:
        print(f"* {RED}FAIL{WHITE} {HEADER}JS exception{WHITE} {round(time.time() - t0, 2)}s")
        page['error'] = type(e).__name__
        fails.append(page)
        remove_directory(download_path)
    except Exception as e:
        print(f"* {RED}FAIL{WHITE} {HEADER}Other exception{WHITE} {round(time.time() - t0, 2)}s")
        print("-" * 100, e, "-" * 100, sep='\n')
        page['error'] = type(e).__name__
        fails.append(page)
        remove_directory(download_path)

    driver.quit()


def process_pages(pages, t0, max_pool, download_path):
    return save_in_parallel(pages, process_routine, t0, max_pool, download_path)
