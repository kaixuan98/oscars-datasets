from scripts.scraper_source.base_scraper import AbstractScraper


class RottenTomatoScraper(AbstractScraper):
    souce_name = "rotten_tomato"
    extended_columns = []

    def load_to_process_data(self, input_path="data/raw/master_list.csv"):
        return super().load_to_process_data(input_path)

    def search_film(self, query):
        return super().search_film(query)

    def extract_match(self, sources, target):
        return super().extract_match(sources, target)

    def extract_score(self, source_url):
        return super().extract_score(source_url)

    def write_to_output(self, row, url, ratings):
        return super().write_to_output(row, url, ratings)
