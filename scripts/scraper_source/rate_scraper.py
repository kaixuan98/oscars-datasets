from abc import ABC, abstractmethod
import os
import os
import traceback
import unicodedata
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from scripts.scraper_source.utils import rate_limit


class AbstractScraper(ABC):
    def __init__(self):
        self.source_name = "base"
        self.driver: WebDriver | None = None
        self.output_path: str | None = None
        self.base_search_path: str | None = None
        self.output_columns = ["master_id", "film", "year_film", "year_ceremony"]
        self.tmdb_search_path = (
            "https://www.themoviedb.org/search/movie?language=en-CA&query="
        )

    def _update_output_columns(self, extended_columns):
        self.output_columns = [*self.output_columns, *extended_columns]

    def run(self) -> None:
        all_rows = []
        self.start_driver()
        to_process_df = self.load_to_process_data()

        for i, row in to_process_df.tail(3).iterrows():
            try:
                query = self.query_formatter(row["film"])
                if self.source_name == "douban":
                    found_tmdb_movies = self.get_film_info(query)
                    found_tmdb_url = self.extract_match(found_tmdb_movies, row)
                    translated_title = self.get_translated_title(found_tmdb_url)
                    search_results = self.search_film(translated_title)
                else:
                    search_results = self.search_film(query)

                found_url = self.extract_match(search_results, row)

                print(row["film"])

                if not found_url:
                    raise Exception(
                        f"No matching film found in top 10 results: {row['film ']} - {row['year_film']}"
                    )

                ratings = self.extract_score(found_url)
                all_rows.append([*row, found_url, *ratings.values()])
            except Exception:
                err = traceback.format_exc()
                print(err)
                with open("logs/errors/error_log.csv", "a", encoding="utf-8") as f:
                    f.write(f"{row['film']},{row['year_film']},{err}\n")
                continue

            # rate_limit(i)
        self.write_to_output(all_rows)
        self.close_driver()
        return

    def query_formatter(self, title: str) -> str:
        """
        Remove all the accents from a given string.
        URL encoding comma and spaces

        """
        clean_str = title.strip().lower().replace(" ", "%20").replace(",", "%2C")
        normalized_str = unicodedata.normalize("NFD", clean_str)
        decoded_str = normalized_str.encode("ascii", errors="ignore").decode("utf-8")
        return decoded_str

    def start_driver(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def get_film_info(self, query) -> list:
        all_searches = []
        self.driver.get(f"{self.tmdb_search_path}{query}")

        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".card.v4.tight")

        # get all the search result
        for s in search_results[:5]:
            try:
                title_elem = s.find_element(By.CSS_SELECTOR, ".title a h2")
                link_elem = s.find_element(By.CSS_SELECTOR, ".title a")
                release_date_elm = s.find_element(
                    By.CSS_SELECTOR, ".title .release_date"
                )

                dt = datetime.strptime(release_date_elm.text, "%B %d, %Y")

                film_url = link_elem.get_attribute("href")
                film_year = dt.year
                film_title = title_elem.text

                all_searches.append(
                    {
                        "url": film_url,
                        "title": film_title,
                        "year": film_year,
                    }
                )

            except Exception:
                continue
        return all_searches

    def get_translated_title(self, url) -> str:
        parts = url.split("?", 1)  # max 1 split
        translations_url = f"{parts[0]}/translations?{parts[1]}"
        self.driver.get(translations_url)
        title_el = self.driver.find_element(
            By.CSS_SELECTOR, "#zh-CN table.media-translations h3"
        )
        title = title_el.text
        return title

    def load_to_process_data(
        self,
        input_path="data/raw/master_list.csv",
    ) -> pd.DataFrame:
        """
        Load the list of data from master to be process
        """
        df = pd.read_csv(input_path)

        if os.path.exists(self.output_path):
            done = pd.read_csv(self.output_path)
        else:
            done = pd.DataFrame(columns=self.output_columns)

        processed_titles = set(zip(done["film"], done["year_film"]))

        to_process = df[
            ~df.apply(lambda x: (x["film"], x["year_film"]) in processed_titles, axis=1)
        ]

        return to_process

    @abstractmethod
    def extract_match(self, sources, target) -> str:
        pass

    @abstractmethod
    def search_film(self, query: str) -> list:
        pass

    @abstractmethod
    def extract_score(self, source_url: str) -> None:
        pass

    @abstractmethod
    def write_to_output(self, data) -> None:
        pass
