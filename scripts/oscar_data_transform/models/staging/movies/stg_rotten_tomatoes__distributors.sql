select
    film as title,
    year_film as release_year,
    year_ceremony,
    distributor,
    lower(film) as title_lower
from
    {{source('scraped_data', 'distributors' )}}