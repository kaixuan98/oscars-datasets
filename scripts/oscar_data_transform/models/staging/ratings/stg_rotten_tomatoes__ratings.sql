select
    film as title,
    lower(film) as title_lower,
    cast(year_film as integer) as release_year,
    year_ceremony,
    rt_url,
    cast(rt_tomatometer as integer),
    cast(rt_critics_count as integer),
    cast(rt_popcornmeter as integer),
    cast(rt_audiences_count as integer)
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/scraped/rt-20260102.csv"
    )