import re
import traceback
import pandas as pd
from datetime import datetime, timezone
from selenium.webdriver.common.by import By
from scripts.scraper_source.rate_scraper import AbstractScraper


class RottenTomatoScraper(AbstractScraper):
    def __init__(self):
        super().__init__()
        self.base_search_path = "https://www.rottentomatoes.com/search?search="
        extract_date = datetime.now(timezone.utc).strftime("%Y%m%d")
        extended_columns = [
            "rt_url",
            "rt_units",
            "rt_tomatometer",
            "rt_critics_count",
            "rt_popcornmeter",
            "rt_audiences_count",
        ]
        self.source_name = "rotten_tomato"
        self.output_path = f"data/scraped/rt_{extract_date}.csv"
        self._update_output_columns(extended_columns)

    def _clean_rt_rating(self, raw: str) -> float:
        cleaned = raw.strip().replace("%", "")
        return float(cleaned)

    def _clean_rt_rating_counts(self, raw: str, type: str) -> float:
        cleaned = raw.strip().replace(",", "")
        if type == "tomatometer":
            num_str = cleaned.split()[0]
            result = float(num_str)
        elif type == "popcornmeter":
            match = re.search(r"\d+", cleaned)
            result = float(match.group(0))
        else:
            result = None

        return result

    def search_film(self, query):
        all_searches = []
        self.driver.get(f"{self.base_search_path}{query}")

        search_results = self.driver.find_elements(
            By.CSS_SELECTOR, "search-page-media-row[data-qa='data-row']"
        )

        for s in search_results[:10]:
            try:
                link_elem = s.find_element(By.CSS_SELECTOR, "a[slot='title']")

                film_url = link_elem.get_attribute("href")
                film_title = link_elem.text.strip()
                film_year = int(s.get_attribute("release-year"))

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
            tomatometer_elem = self.driver.find_element(
                By.CSS_SELECTOR, "rt-text[slot='criticsScore']"
            )
            popcornmeter_elem = self.driver.find_element(
                By.CSS_SELECTOR, "rt-text[slot='audienceScore']"
            )

            tomatometer_count_elem = self.driver.find_element(
                By.CSS_SELECTOR, "rt-link[slot='criticsReviews']"
            )
            popcornmeter_count_elem = self.driver.find_element(
                By.CSS_SELECTOR, "rt-link[slot='audienceReviews']"
            )

            return {
                "rt_units": "percentage",
                "rt_tomatometer": self._clean_rt_rating(tomatometer_elem.text),
                "rt_critics_count": self._clean_rt_rating_counts(
                    tomatometer_count_elem.text, "tomatometer"
                ),
                "rt_popcornmeter": self._clean_rt_rating(popcornmeter_elem.text),
                "rt_audiences_count": self._clean_rt_rating_counts(
                    popcornmeter_count_elem.text, "popcornmeter"
                ),
            }

        except Exception:
            print(traceback.format_exc())

    def write_to_output(self, data):
        # remove the index
        df = pd.DataFrame([*data], columns=self.output_columns)
        df.to_csv(self.output_path, index=False)
