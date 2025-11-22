from abc import ABC, abstractmethod
import traceback
import unicodedata
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from scripts.scraper_source.utils import rate_limit


class AbstractScraper(ABC):
    def __init__(self):
        self.source_name = "base"
        self.output_columns = ["film", "year_film", "year_ceremony"]
        self.driver: WebDriver | None = None
        self.output_path: str | None = None
        self.base_search_path: str | None = None

    def _update_output_columns(self, extended_columns):
        self.output_columns = [*self.output_columns, *extended_columns]

    def run(self) -> None:
        self.start_driver()
        to_process_df = self.load_to_process_data()
        for i, row in to_process_df.tail(3).iterrows():
            print("processing: ", row["film"])
            try:
                query = self.query_formatter(row["film"])
                search_results = self.search_film(query)
                found_url = self.extract_match(search_results, row)

                if not found_url:
                    raise Exception(
                        f"No matching film found in top 10 results: {row['film ']} - {row['year_film']}"
                    )

                ratings = self.extract_score(found_url)

                print(ratings)
                # self.write_to_output(row, found_url, ratings)
            except Exception:
                err = traceback.format_exc()
                print(err)
                # with open(
                #     "logs/errors/letterbox_error_log.csv", "a", encoding="utf-8"
                # ) as f:
                #     f.write(f"{row['film']},{row['year_film']},{err}\n")
                continue

            # rate_limit(i)
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

    @abstractmethod
    def load_to_process_data(
        self,
        input_path="data/raw/master_list.csv",
    ) -> pd.DataFrame:
        """
        Load the list of data from master to be process
        """
        pass

    @abstractmethod
    def search_film(self, query: str) -> list:
        pass

    @abstractmethod
    def extract_match(self, sources, target) -> str:
        pass

    @abstractmethod
    def extract_score(self, source_url: str) -> None:
        pass

    @abstractmethod
    def write_to_output(self, row, url: str, ratings) -> None:
        pass
