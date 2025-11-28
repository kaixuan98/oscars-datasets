import os
import traceback
import pandas as pd
from scripts.scraper_source.utils import make_driver
from selenium.webdriver.common.by import By

driver = make_driver()
input_path = f"{os.getcwd()}/data/raw/master_list_rt.csv"
output_path = f"{os.getcwd()}/data/scraped/distributors.csv"
output_columns = ["film", "year_film", "year_ceremony", "imdb_id"]


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
    df_columns = to_process_df.columns.to_list()

    for i, row in to_process_df.tail(3).iterrows():
        try:
            driver.get(row["rt_url"])

            block = driver.find_element(
                By.XPATH,
                "//div[@class='category-wrap' and @data-qa='item'][.//rt-text[text()='Distributor']]",
            )
            distributor = block.find_element(
                By.XPATH, ".//rt-text[@data-qa='item-value']"
            )

            all_rows.append([*row, distributor.text])
        except Exception:
            err = traceback.format_exc()
            print(err)
            with open("logs/errors/error_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{row['film']},{row['year_film']},{err}\n")
            continue

        # rate_limit(i)
    df = pd.DataFrame([*all_rows], columns=[*df_columns, "distributor"])
    df.to_csv("data/scraped/distributors.csv", index=False)
    driver.quit()
    return
