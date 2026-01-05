import csv
import logging
import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from scripts.driver_manager import DriverManager
from scripts.scraper_source.awards.award_scrapper_strategy import (
    AwardScraperStrategy,
)
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scripts.scraper_source.utils import rate_limit


class GoldenGlobeStrategy(AwardScraperStrategy):
    def __init__(self):
        super().__init__()
        self.base_url = "https://goldenglobes.com/winners-nominees/"
        self.output_file = "data/scraped/golden_globes.csv"
        self.driver = DriverManager().create_web_driver()

    def extract(self, years):
        logger = logging.getLogger(__name__)
        logger.info("Start extracting golden globe")

        try:
            all_nominees = []

            # get each year best picture in drama and comedy
            for i, y in enumerate(years):
                self.driver.get(self.base_url)

                # select the dropdown button
                dropdownBtn = self.driver.find_element(By.ID, "year")
                select = Select(dropdownBtn)
                select.select_by_value(y)

                # wait for the page to fetch and load
                wait = WebDriverWait(self.driver, 20)
                wait.until_not(
                    EC.visibility_of_all_elements_located(
                        (
                            By.CSS_SELECTOR,
                            "div.c-winner-nominees_loading",
                        )
                    )
                )

                # pass the page to beautiful soup and extract it
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # get all the categories
                category_divs = soup.select("div.c-winner-nominees-group")[:2]

                for category_div in category_divs:
                    # Get category name from <h3>
                    category_name_tag = category_div.select_one(
                        "h3.c-winner-nominees-group__title"
                    )
                    category_name = category_name_tag.get_text(strip=True)

                    # Loop over all nominees/winners in this category
                    for li in category_div.select("li.c-winner-nominees-group-item"):
                        title_tag = li.select_one(
                            "h4.c-winner-nominees-group-item__title a"
                        )
                        title = title_tag.get_text(strip=True)

                        # Determine if winner
                        is_winner = "is-active" in li.get("class", [])

                        all_nominees.append(
                            {
                                "year": y,
                                "category": category_name,
                                "title": title,
                                "is_winner": is_winner,
                            }
                        )

                rate_limit(i)
            # output the data into a csv file
            fieldnames = all_nominees[0].keys()

            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()  # write header row
                writer.writerows(all_nominees)  # write all rows

        except Exception:
            logger.exception("Error scraping golden globe")
