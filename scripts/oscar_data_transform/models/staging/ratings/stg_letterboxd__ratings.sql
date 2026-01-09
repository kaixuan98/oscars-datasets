select
    film as title,
    lower(film) as title_lower,
    year_film as release_year,
    year_ceremony,
    lb_url,
    cast(lb_rating as double),
    cast(lb_rating_count as integer),
    cast(lb_watched_by as integer),
    cast(lb_liked_by as integer)
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/scraped/lb_20260102.csv"
    )