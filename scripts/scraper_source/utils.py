import time
import logging
from pathlib import Path
from selenium import webdriver
from logging.handlers import RotatingFileHandler
from selenium.webdriver.chrome.options import Options


def make_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    return driver


def rate_limit(i, batch_size=10, sleep_seconds=300):
    logger = logging.getLogger(__name__)
    if i > 0 and i % batch_size == 0:
        logger.info("Rate Limiting: sleeping for %s seconds ...", sleep_seconds)
        time.sleep(sleep_seconds)


def setup_logging(log_file: str = "logs/scraper.log", level: int = logging.INFO):
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = RotatingFileHandler(log_path, maxBytes=5_000_000, backupCount=5)

    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
