import csv
import traceback
from bs4 import BeautifulSoup
import wikipedia
from scripts.scraper_source.awards.award_scrapper_strategy import AwardScraperStrategy


class BaftaStrategy(AwardScraperStrategy):
    def __init__(self):
        super().__init__()
        self.type = "bafta"
        self.output_file = "data/scraped/bafta.csv"

    def extract(self, years: list[str]):
        print("Start extracting bafta")
        all_nominees = []

        try:
            page = wikipedia.page("BAFTA Award for Best Film")
            soup = BeautifulSoup(page.html(), "html.parser")

            tables = soup.find_all("table", class_="wikitable")

            for table in tables:
                current_year = None
                rows = table.find_all("tr")
                if not rows:
                    continue

                for row in rows:
                    cells = row.find_all(["th", "td"])
                    # get year
                    if cells[0].has_attr("rowspan"):
                        current_year = cells[0].get_text(strip=True).split()[0]
                        film_td = cells[1]
                    else:
                        film_td = cells[0]

                    # get film title
                    film_link = film_td.find("a")
                    if not film_link:
                        continue
                    film_title = film_link.get_text(strip=True)

                    is_winner = "background:#FAEB86" in film_td.get("style", "")

                    all_nominees.append(
                        {
                            "year": current_year,
                            "film": film_title,
                            "is_winner": is_winner,
                        }
                    )
            fieldnames = all_nominees[0].keys()

            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()  # write header row
                writer.writerows(all_nominees)  # write all rows

        except Exception:
            err = traceback.format_exc()
            print(err)
