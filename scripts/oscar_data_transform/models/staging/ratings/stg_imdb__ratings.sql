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
    cast(imdb_rating as double) as imdb_rating,
    cast(imdb_votes as integer) as imdb_rating_count,
from
    read_csv_auto(
        "/Users/kaixuanchin/Code/oscars-datasets/data/raw/TMDB_all_movies.csv"
    )
where
    release_date > '1989-01-01'