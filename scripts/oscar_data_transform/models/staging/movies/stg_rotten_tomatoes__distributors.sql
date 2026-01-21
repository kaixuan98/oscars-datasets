select
    film as title,
    year_film as release_year,
    year_ceremony,
    distributor,
    REGEXP_REPLACE(lower(film), '[^a-zA-Z0-9]', '', 'g') as title_lower
from
    {{source('scraped_data', 'distributors' )}}