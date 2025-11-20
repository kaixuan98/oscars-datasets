from datetime import datetime, timezone
import os
import re
import traceback
import pandas as pd
from selenium.webdriver.common.by import By
from scripts.scraper_source.utils import make_driver, rate_limit

driver = make_driver()
letterbox_search = "https://letterboxd.com/search/films"


# ---------------- helpers -------------------------
def reformat(title, replacement):
    result = title.lower().replace(" ", replacement)
    return result


def search_letterbox(title: str):
    all_searches = []
    query = reformat(title, "+")
    driver.get(f"{letterbox_search}/{query}")

    result_list = driver.find_element(By.CLASS_NAME, "results")
    search_results = result_list.find_elements(By.TAG_NAME, "li")

    for s in search_results[:10]:
        try:
            link_elem = s.find_element(By.CSS_SELECTOR, "h2 a")
            year_elem = s.find_element(By.CSS_SELECTOR, "h2 small.metadata a")

            film_url = link_elem.get_attribute("href")
            film_title = link_elem.text.strip()
            film_year = int(year_elem.text.strip())
            all_searches.append(
                {"url": film_url, "title": film_title, "year": film_year}
            )
        except Exception:
            continue

    return all_searches


def extract_match(sources, target):
    sources_df = pd.DataFrame(sources)
    clean_source_title = (
        sources_df["title"]
        .str.strip()
        .str.lower()
        .str.replace("’", "")
        .str.replace("'", "")
    )
    clean_target_title = (
        target["film"].strip().lower().replace("’", "").replace("'", "")
    )
    filtered_films = sources_df[
        (clean_source_title == clean_target_title)
        & (sources_df["year"] == target["year_film"])
    ]

    # if more than 1 results, get first value of the list
    found_url = None
    if len(filtered_films) > 0:
        found_url = filtered_films.iloc[0]["url"]

    return found_url


def extract_score(url):
    driver.get(url)

    rating_tag = driver.find_element(By.CSS_SELECTOR, "a.display-rating")
    tooltip_text = rating_tag.get_attribute("data-original-title")

    match = re.search(r"based on ([\d,]+) ratings", tooltip_text)
    if match:
        rating_count = int(match.group(1).replace(",", ""))
    else:
        rating_count = None

    return {"rating": float(rating_tag.text), "rating_count": rating_count}


# ----------- functions ---------------------
def run_letterbox_scraper():
    extract_date = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    master_list_path = "data/master_list.csv"
    output_path = f"data/letterbox_score__{extract_date}.csv"

    df = pd.read_csv(master_list_path)

    # load processed data
    if os.path.exists(output_path):
        done = pd.read_csv(output_path)
    else:
        done = pd.DataFrame(
            columns=[
                "film",
                "year_film",
                "year_ceremony",
                "lb_url",
                "lb_rating",
                "lb_rating_count",
            ]
        )

    processed_titles = set(zip(done["film"], done["year_film"]))

    to_process = df[
        ~df.apply(lambda x: (x["film"], x["year_film"]) in processed_titles, axis=1)
    ]

    for i, row in to_process.iterrows():
        print(f"Processing: {row['film']} - {row['year_film']}")

        try:
            search_results = search_letterbox(row["film"])
            found_url = extract_match(search_results, row)

            if not found_url:
                raise Exception("No matching film found in top 10 results")

            rating = extract_score(found_url)

            new_row = pd.DataFrame(
                [
                    [
                        row["film"],
                        row["year_film"],
                        row["year_ceremony"],
                        found_url,
                        rating["rating"],
                        rating["rating_count"],
                    ]
                ],
                columns=[
                    "film",
                    "year_film",
                    "year_ceremony",
                    "url",
                    "rating",
                    "rating_count",
                ],
            )
            new_row.to_csv(output_path, mode="a", header=False, index=False)
        except Exception:
            err = traceback.format_exc()
            with open("letterbox_error_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{row['film']},{row['year_film']},{err}\n")
            continue

        rate_limit(i)

    driver.quit()

    return
