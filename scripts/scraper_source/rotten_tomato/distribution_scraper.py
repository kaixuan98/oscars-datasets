import os
import traceback
from bs4 import BeautifulSoup
import pandas as pd
from scripts.scraper_source.utils import make_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = make_driver()
input_path = f"{os.getcwd()}/data/raw/master_list_imdb.csv"
output_path = f"{os.getcwd()}/data/scraped/imdb_distributors.csv"
output_columns = ["film", "year_film", "year_ceremony", "imdb_id"]
base_url = "https://www.imdb.com/title/"


def load__to_process__data():
    df = pd.read_csv(input_path)

    if os.path.exists(output_path):
        done = pd.read_csv(output_path)
    else:
        done = pd.DataFrame(columns=output_columns)

    processed_titles = set(zip(done["film"], done["year_film"]))

    to_process = df[
        ~df.apply(lambda x: (x["film"], x["year_film"]) in processed_titles, axis=1)
    ]

    return to_process


def run_distribution_scraper() -> None:
    all_rows = []
    to_process_df = load__to_process__data()

    for i, row in to_process_df.tail(3).iterrows():
        try:
            # build imdb url + fetch the page
            film_url = f"{base_url}{row['imdb_id']}/companycredits"
            driver.get(film_url)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            print(soup.prettify())

            distribution_list = driver.find_element(
                By.CSS_SELECTOR,
                "div[role='presentation']",
            )
            print(distribution_list)

            # all_rows.append([*row, found_url, *ratings.values()])
        except Exception:
            err = traceback.format_exc()
            print(err)
            with open("logs/errors/error_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{row['film']},{row['year_film']},{err}\n")
            continue

        # rate_limit(i)
    # write_to_output(all_rows)
    driver.quit()
    return
