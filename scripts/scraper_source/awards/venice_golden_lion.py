import csv
import traceback
from bs4 import BeautifulSoup
import wikipedia
from scripts.scraper_source.awards.award_scrapper_strategy import AwardScraperStrategy


class VeniceGoldenLionStrategy(AwardScraperStrategy):
    def __init__(self):
        super().__init__()
        self.output_file = "data/scraped/venice_golden_lion.csv"

    def extract(self, years: list[str]):
        print("Start extracting golden lion")
        all_nomimees = []
        try:
            page = wikipedia.page("Golden Lion")
            soup = BeautifulSoup(page.html(), "html.parser")

            tables = soup.find_all("table", class_="wikitable")

            for table in tables:
                current_year = None
                rows = table.find_all("tr")
                if not rows:
                    continue

                for row in rows:
                    # get year
                    year_th = row.find("th")
                    film_td = row.find("td")
                    if not year_th or not film_td:
                        continue
                    current_year = year_th.get_text(strip=True)

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
