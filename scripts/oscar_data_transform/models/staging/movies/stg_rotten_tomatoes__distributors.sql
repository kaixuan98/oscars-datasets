select
    film as title,
    year_film as release_year,
    year_ceremony,
    distributor
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/scraped/distributors.csv"
    )