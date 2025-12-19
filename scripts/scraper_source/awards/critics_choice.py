import csv
import traceback
from bs4 import BeautifulSoup
import wikipedia
from scripts.scraper_source.awards.award_scrapper_strategy import (
    AwardScraperStrategy,
)


class CriticsChoiceStrategy(AwardScraperStrategy):
    def __init__(self):
        super().__init__()
        self.base_url = "https://en.wikipedia.org/wiki/Critics%27_Choice_Movie_Award_for_Best_Picture"
        self.output_file = "data/scraped/critics_choice.csv"

    def extract(self, years: list[str]):
        print("Start extracting critics choice")
        all_nominees = []
        try:
            page = wikipedia.page("Critics' Choice Movie Award for Best Picture")
            soup = BeautifulSoup(page.html(), "html.parser")

            tables = soup.find_all("table", class_="wikitable")

            for table in tables:
                for row in table.find_all("tr"):
                    # get the year
                    th = row.find("th")
                    if th and th.find("a"):
                        current_year = th.get_text(strip=True)

                    # get film column
                    tds = row.find_all("td")
                    if not tds:
                        continue
                    film_td = tds[0]
                    film_link = film_td.find("a")
                    if not film_link:
                        continue

                    film_title = film_link.get_text(strip=True)

                    # get winner
                    is_winner = "background:#B0C4DE" in film_td.get("style", "")

                    all_nominees.append(
                        {
                            "year": current_year,
                            "film": film_title,
                            "is_winner": is_winner,
                        }
                    )
            # output the data into a csv file
            fieldnames = all_nominees[0].keys()

            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()  # write header row
                writer.writerows(all_nominees)  # write all rows

        except Exception:
            err = traceback.format_exc()
            print(err)
