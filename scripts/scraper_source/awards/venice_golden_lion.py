import csv
import traceback
from bs4 import BeautifulSoup
import wikipedia
from scripts.scraper_source.awards.award_scrapper_strategy import AwardScraperStrategy


class VeniceGoldenLionStrategy(AwardScraperStrategy):
    def __init__(self):
        super().__init__()
        self.output_file = "data/scraped/venice_golden_lion.csv"

    def __get_wikitables_for_winners_section(self, soup):
        h2 = soup.find("h2", id="Winners")
        if not h2:
            return []

        tables = []

        for elem in h2.parent.find_next_siblings():
            # Stop when next section starts
            if elem.name == "div" and elem.find("h2"):
                break

            if elem.name == "table" and "wikitable" in elem.get("class", []):
                tables.append(elem)

        return tables

    def extract(self, years: list[str]):
        print("Start extracting golden lion")
        all_nomimees = []
        try:
            page = wikipedia.page("Golden Lion")
            soup = BeautifulSoup(page.html(), "html.parser")

            tables = self.__get_wikitables_for_winners_section(soup)

            for table in tables:
                current_year = None
                rows = table.find_all("tr")
                if not rows:
                    continue

                for row in rows:
                    cells = row.find_all(["th", "td"])
                    if not cells:
                        continue

                    # get year
                    if (
                        cells[0].name in ["th", "td"]
                        and cells[0].get_text(strip=True).isdigit()
                    ):
                        current_year = cells[0].get_text(strip=True)
                        if len(cells) > 1:
                            film_td = cells[1]
                        else:
                            continue
                    else:
                        film_td = cells[0]

                    # get film title
                    film_link = film_td.find("a")
                    if not film_link:
                        continue
                    film_title = film_link.get_text(strip=True)

                    all_nomimees.append({"year": current_year, "film": film_title})

            fieldnames = all_nomimees[0].keys()

            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()  # write header row
                writer.writerows(all_nomimees)  # write all rows

        except Exception:
            err = traceback.format_exc()
            print(err)
