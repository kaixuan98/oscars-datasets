from abc import ABC, abstractmethod


class AbstractScraper(ABC):
    source_name = "base"

    # this the method will run the whole process - the algorithm
    def template_method(self) -> None:
        self.query_formater()

    # operation already have implementation
    # extract the master file

    # output the file
    # query reformater
    # get web driver

    # operation that need to implement in the subclass
    @abstractmethod
    def query_formatter(self, title: str) -> str:
        # comma -> %2C
        # space -> %20

        pass

    @abstractmethod
    def search_film(self) -> None:
        pass

    @abstractmethod
    def extract_match(self) -> None:
        pass

    @abstractmethod
    def extract_score(self) -> None:
        pass
