import re
import traceback
from scripts.scraper_source.rate_scraper import AbstractScraper
from selenium.webdriver.common.by import By
from datetime import datetime, timezone
import pandas as pd


class LetterboxScraper(AbstractScraper):
    def __init__(self):
        super().__init__()
        self.source_name = "letterbox"
        self.base_search_path = "https://letterboxd.com/search/films"
        extract_date = datetime.now(timezone.utc).strftime("%Y%m%d")
        extended_columns = [
            "lb_url",
            "lb_rating_outof",
            "lb_rating",
            "lb_rating_count",
            "lb_watched_by",
            "lb_liked_by",
        ]
        self.output_path = f"data/scraped/lb_{extract_date}.csv"
        self._update_output_columns(extended_columns)

    def _extract_numbers(self, s: str):
        nums = re.findall(r"[\d.,]+", s)
        result = []
        for n in nums:
            result.append(float(n.replace(",", "")))
        return result

    def search_film(self, query):
        all_searches = []
        self.driver.get(f"{self.base_search_path}/{query}")

        result_list = self.driver.find_element(By.CLASS_NAME, "results")
        search_results = result_list.find_elements(By.TAG_NAME, "li")

        for s in search_results[:10]:
            try:
                link_elem = s.find_element(By.CSS_SELECTOR, "h2 a")
                year_elem = s.find_element(By.CSS_SELECTOR, "h2 small.metadata a")

                film_url = link_elem.get_attribute("href")
                film_title = link_elem.text.strip()
                film_year = int(year_elem.text.strip())
                all_searches.append(
                    {"url": film_url, "title": film_title, "year": film_year}
                )
            except Exception:
                continue

        return all_searches

    def extract_match(self, sources, target):
        sources_df = pd.DataFrame(sources)
        clean_source_title = (
            sources_df["title"]
            .str.strip()
            .str.lower()
            .str.replace("’", "")
            .str.replace("'", "")
        )
        clean_target_title = (
            target["film"].strip().lower().replace("’", "").replace("'", "")
        )
        year_diff = sources_df["year"] - int(target["year_film"])

        filtered_films = sources_df[
            (clean_source_title == clean_target_title)
            & ((year_diff <= 1) & (year_diff >= -1))
        ]
        found_url = None
        if len(filtered_films) > 0:
            found_url = filtered_films.iloc[0]["url"]
        else:
            found_url = sources_df.iloc[0]["url"]

        return found_url

    def extract_score(self, source_url):
        self.driver.get(source_url)

        try:
            rating_tag = self.driver.find_element(By.CSS_SELECTOR, "a.display-rating")
            tooltip_text = rating_tag.get_attribute("data-original-title")
            watches_elem = self.driver.find_element(
                By.CSS_SELECTOR, "div.production-statistic.-watches a.tooltip"
            )
            likes_elem = self.driver.find_element(
                By.CSS_SELECTOR, "div.production-statistic.-likes a.tooltip"
            )

            watched_count_raw = watches_elem.get_attribute("data-original-title")
            likes_count_raw = likes_elem.get_attribute("data-original-title")

            rating, rating_count = self._extract_numbers(tooltip_text)
            watched = self._extract_numbers(watched_count_raw)[0]
            liked = self._extract_numbers(likes_count_raw)[0]

        except Exception:
            print(traceback.format_exc())

        return {
            "lb_rating": rating,
            "lb_rating_count": rating_count,
            "lb_rating_outof": 5.0,
            "lb_watched_by": watched,
            "lb_liked_by": liked,
        }

    def write_to_output(self, data):
        df = pd.DataFrame([*data], columns=self.output_columns)
        df.to_csv(self.output_path, mode="a", index=False)
