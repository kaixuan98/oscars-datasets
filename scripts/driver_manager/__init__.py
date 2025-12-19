from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverManager:
    def __init__(self):
        self.driver = None

    def create_web_driver(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        return self.driver

    def close_web_driver(self):
        if self.driver:
            self.driver.quit()
