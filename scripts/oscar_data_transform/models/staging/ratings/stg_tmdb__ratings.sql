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
    imdb_id,
    cast(vote_average as integer) as tmdb_user_score,
    cast(vote_count as integer) as tmdb_user_score_count,
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/raw/TMDB_all_movies.csv"
    )
where
    release_date > '1989-01-01'