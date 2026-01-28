select
    title,
    REGEXP_REPLACE(lower(title), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    release_date,
    extract(
        'year'
        FROM
            release_date
    ) as release_year,
    imdb_id,
    cast(vote_average as double) as tmdb_user_score,
    cast(vote_count as integer) as tmdb_user_score_count,
from
    {{source('raw_data', 'TMDB_all_movies')}}
where
    release_date > '1989-01-01'