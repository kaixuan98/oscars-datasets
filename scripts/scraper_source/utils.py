import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def make_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    return driver


def rate_limit(i, batch_size=10, sleep_seconds=300):
    if i > 0 and i % batch_size == 0:
        print(f"Rate Limiting: sleeping for {sleep_seconds} seconds ...")
        time.sleep(sleep_seconds)
