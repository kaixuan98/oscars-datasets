select
    film as title,
    lower(film) as title_lower,
    year_film as release_year,
    year_ceremony,
    lb_url as letterboxd_url,
    cast(lb_rating as double) as letterboxd_rating,
    cast(lb_rating_count as integer) as letterboxd_rating_count,
    cast(lb_watched_by as integer) as letterboxd_watched,
    cast(lb_liked_by as integer) as letterboxd_liked
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/scraped/lb_20260102.csv"
    )