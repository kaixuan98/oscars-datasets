import csv
import traceback

from bs4 import BeautifulSoup
import wikipedia
from scripts.scraper_source.awards.award_scrapper_strategy import AwardScraperStrategy


class ScreenActorGuildStrategy(AwardScraperStrategy):
    def __init__(self):
        super().__init__()
        self.base_url = "https://en.wikipedia.org/wiki/Screen_Actors_Guild_Award_for_Outstanding_Performance_by_a_Cast_in_a_Motion_Picture"
        self.output_file = "data/scraped/screen_actor_guild.csv"

    def extract(self, years: list[str]):
        print("Start extracting screen actor guild")
        all_nomimees = []
        try:
            page = wikipedia.page(
                "Screen Actors Guild Award for Outstanding Performance by a Cast in a Motion Picture"
            )
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

                    # get winner
                    is_winner = "background:#FAEB86" in film_td.get("style", "")

                    all_nomimees.append(
                        {
                            "year": current_year,
                            "film": film_title,
                            "is_winner": is_winner,
                        }
                    )

            fieldnames = all_nomimees[0].keys()

            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()  # write header row
                writer.writerows(all_nomimees)  # write all rows

        except Exception:
            err = traceback.format_exc()
            print(err)
