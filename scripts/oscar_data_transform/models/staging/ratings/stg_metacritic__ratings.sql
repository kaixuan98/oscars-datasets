select
    film as title,
    lower(film) as title_lower,
    cast(year_film as integer) as release_year,
    year_ceremony,
    mc_url,
    cast(mc_metascore as integer) as mc_metascore,
    cast(mc_metascore_count as integer) as mc_metascore_count,
    cast(mc_users_score as double) as mc_users_score,
    cast(mc_users_count as integer) as mc_users_count
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/scraped/mc_20260102.csv"
    )