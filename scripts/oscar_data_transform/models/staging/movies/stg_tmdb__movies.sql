select
    id as movie_id,
    title,
    REGEXP_REPLACE(lower(title), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    release_date,
    extract(
        'year'
        FROM
            release_date
    ) as release_year,
    revenue,
    runtime,
    budget,
    imdb_id,
    original_language,
    overview,
    genres,
    production_companies,
    spoken_languages,
    "cast" as cast_members,
    director,
    director_of_photography,
    writers,
    producers,
    music_composer,
    poster_path
from
    {{source('raw_data', 'TMDB_all_movies')}}
where
    release_date > '1989-01-01'