select
    film as title,
    REGEXP_REPLACE(lower(film), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    cast(year_film as integer) as release_year,
    lb_url,
    cast(lb_rating_outof as double) as rating,
    cast(lb_rating as integer) as rating_count,
    cast(lb_watched_by as integer) as watched_count,
    cast(lb_liked_by as integer) as liked_count
from
    {{ source('scraped_data', 'lb_20260102')}}
