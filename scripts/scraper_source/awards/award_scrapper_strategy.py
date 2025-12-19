from abc import ABC, abstractmethod


class AwardScraperStrategy(ABC):
    @abstractmethod
    def extract(self, decades: list[int]):
        pass
