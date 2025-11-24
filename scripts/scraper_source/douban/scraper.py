from datetime import datetime, timezone
from selenium.webdriver.common.by import By
from scripts.scraper_source.base_scraper import AbstractScraper


class DoubanScraper(AbstractScraper):
    def __init__(self):
        super().__init__()
        self.source_name = "douban"
        self.base_search_path = "https://www.douban.com/search?cat=1002&q="
        extract_date = datetime.now(timezone.utc).strftime("%Y%m%d")
        extended_columns = [
            "film_zh_cn",
            "douban_url",
            "douban_score",
            "douban_score_count",
        ]
        self.output_path = f"data/scraped/douban_{extract_date}.csv"
        self._update_output_columns(extended_columns)

    def search_film(self, query):
        return super().search_film(query)

    def extract_match(self, sources, target):
        return super().extract_match(sources, target)

    def extract_score(self, source_url):
        return super().extract_score(source_url)

    def write_to_output(self, data):
        return super().write_to_output(data)
