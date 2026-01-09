select
    film as title,
    lower(film) as title_lower,
    cast(year_film as integer) as release_year,
    year_ceremony,
    lb_url,
    cast(lb_rating as double) as lb_rating,
    cast(lb_rating_count as integer) as lb_rating_count,
    cast(lb_watched_by as integer) as lb_watched_by,
    cast(lb_liked_by as integer) as lb_liked_by
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/scraped/lb_20260102.csv"
    )