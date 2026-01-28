select
    title,
    REGEXP_REPLACE(lower(title), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    extract(
        'year'
        FROM
            release_date
    ) as release_year,
    imdb_id,
    cast(imdb_rating as double) as rating,
    cast(imdb_votes as integer) as rating_count,
from
    {{source('raw_data', 'TMDB_all_movies')}}
where
    release_date > '1989-01-01'