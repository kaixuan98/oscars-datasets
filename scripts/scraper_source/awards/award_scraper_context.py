# this class provides a context for the award scrapper interface
# When client call, they will do AwardScraperContext(GoldenGloabStrategy())
# so they get access to run the scraper with a golden globe strategy


from scripts.scraper_source.awards.award_scrapper_strategy import (
    AwardScraperStrategy,
)


class AwardScraperContext:
    def __init__(self, strategy: AwardScraperStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> AwardScraperStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AwardScraperStrategy) -> None:
        self._strategy = strategy

    # context will run the strategy
    def process_extraction(self) -> None:
        years = ["2025", "2024"]
        self.strategy.extract(years)
