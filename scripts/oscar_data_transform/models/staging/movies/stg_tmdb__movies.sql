select
    id as movie_id,
    title,
    lower(title) as title_lower,
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
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/raw/TMDB_all_movies.csv"
    )
where
    release_date > '1989-01-01'