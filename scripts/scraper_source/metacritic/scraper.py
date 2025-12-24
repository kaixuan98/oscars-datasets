from datetime import datetime, timezone
import re
import traceback
import pandas as pd
from selenium.webdriver.common.by import By
from scripts.scraper_source.rate_scraper import AbstractScraper


class MetacriticScraper(AbstractScraper):
    def __init__(self):
        super().__init__()
        self.source_name = "metacritic"
        self.base_search_path = "https://www.metacritic.com/search/"
        self.base_search_query = "/?page=1&category=2"
        extract_date = datetime.now(timezone.utc).strftime("%Y%m%d")
        extended_columns = [
            "mc_url",
            "mc_metascore",
            "mc_metascore_count",
            "mc_metascore_outof",
            "mc_metascore_sentiment",
            "mc_users_score",
            "mc_users_count",
            "mc_users_score_outof",
            "mc_user_score_sentiment",
        ]
        self.output_path = f"data/scraped/mc_{extract_date}.csv"
        self._update_output_columns(extended_columns)

    def _clean_mc_rating(self, raw: str) -> float:
        # example: "Metascore 91 out of 100" or "User score 7.3 out of 10"
        match = re.search(r"\d+(\.\d+)?", raw)
        if match:
            number = match.group()
            first_int = float(number)
        return first_int

    def _clean_mc_rating_counts(self, raw: str) -> float:
        match = re.search(r"\d[\d,]*", raw)
        number = float(match.group().replace(",", ""))
        return number

    def search_film(self, query):
        all_searches = []
        self.driver.get(f"{self.base_search_path}{query}{self.base_search_query}")

        search_results_wrapper = self.driver.find_element(
            By.CSS_SELECTOR, ".c-pageSiteSearch-results"
        )
        search_results = search_results_wrapper.find_elements(
            By.CSS_SELECTOR, 'a[data-testid="search-result-item"]'
        )

        for s in search_results[:10]:
            try:
                title_elem = s.find_element(
                    By.CSS_SELECTOR, 'p[data-testid="product-title"]'
                )
                date_elem = s.find_element(
                    By.CSS_SELECTOR, 'span[data-testid="product-release-date"]'
                )

                film_url = s.get_attribute("href")
                film_title = title_elem.text
                film_year = int(date_elem.text.split(",")[1].strip())

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
            # get both score container
            metascore_container = self.driver.find_element(
                By.CSS_SELECTOR, 'div[data-testid="critic-score-info"]'
            )
            userscore_container = self.driver.find_element(
                By.CSS_SELECTOR, 'div[data-testid="user-score-info"]'
            )

            metascore = metascore_container.find_element(
                By.CSS_SELECTOR, ".c-siteReviewScore"
            ).get_attribute("title")
            metascore_sentiment = metascore_container.find_element(
                By.CSS_SELECTOR, ".c-productScoreInfo_scoreSentiment "
            ).text
            metascore_total = metascore_container.find_element(
                By.CSS_SELECTOR, ".c-productScoreInfo_reviewsTotal"
            ).text

            userscore = userscore_container.find_element(
                By.CSS_SELECTOR, ".c-siteReviewScore"
            ).get_attribute("title")
            userscore_sentiment = userscore_container.find_element(
                By.CSS_SELECTOR, ".c-productScoreInfo_scoreSentiment "
            ).text
            userscore_total = userscore_container.find_element(
                By.CSS_SELECTOR, ".c-productScoreInfo_reviewsTotal"
            ).text

            return {
                "mc_metascore": self._clean_mc_rating(metascore),
                "mc_metascore_count": self._clean_mc_rating_counts(metascore_total),
                "mc_metascore_outof": 100,
                "mc_metascore_sentiment": metascore_sentiment,
                "mc_users_score": self._clean_mc_rating(userscore),
                "mc_users_count": self._clean_mc_rating_counts(userscore_total),
                "mc_users_score_outof": 10,
                "mc_user_score_sentiment": userscore_sentiment,
            }

        except Exception:
            print(traceback.format_exc())

        return

    def write_to_output(self, data):
        df = pd.DataFrame([*data], columns=self.output_columns)
        df.to_csv(self.output_path, mode="a", index=False)
