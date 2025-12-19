from abc import ABC, abstractmethod


class AwardScraperStrategy(ABC):
    @abstractmethod
    def extract(self, years):
        pass
