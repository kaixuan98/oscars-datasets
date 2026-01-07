SELECT
    *
from
    "data/raw/the_oscar_award.csv"
LIMIT
    5;

describe table "data/raw/TMDB_all_movies.csv";

describe table "data/raw/the_oscar_award.csv";

-- get all the title within certain relase date
SELECT
    title
from
    "data/raw/TMDB_all_movies.csv"
where
    release_date > '2024-01-01'
    and release_date < '2025-01-01';

-- get all best picture nom for year 2025
SELECT distinct
    *
from
    "data/raw/the_oscar_award.csv"
where
    year_ceremony = 2025
    AND canon_category = 'BEST PICTURE';

-- get all bess picture from 2001 to 2025
select
    *
from
    'data/raw/the_oscar_award.csv'
where
    canon_category = 'BEST PICTURE'
    AND year_ceremony > 1999
    AND year_ceremony < 2025;

-- imdb rating, budget and revenue for all best picture 2025
-- budget estimated, revenue is gross worldwide
SELECT
    title,
    budget,
    revenue,
    imdb_rating,
    imdb_votes,
    genres,
    imdb_id
from
    "data/raw/TMDB_all_movies.csv"
where
    title in (
        SELECT distinct
            film
        from
            "data/raw/the_oscar_award.csv"
        where
            year_ceremony = 2025
            AND canon_category = 'BEST PICTURE'
    )
    AND release_date > '2024-01-01'
    AND release_date < '2025-03-01'
    AND vote_average > 0
ORDER BY
    vote_average DESC;

-- calculate how many nomintion in the academy
SELECT
    film,
    STRING_AGG (
        canon_category,
        ', '
        ORDER BY
            canon_category
    ) AS nominations,
    COUNT(*) AS nomination_count,
    COUNT(
        CASE
            WHEN winner = TRUE THEN 1
        END
    ) AS true_count
FROM
    "data/raw/the_oscar_award.csv"
WHERE
    film IN (
        SELECT DISTINCT
            film
        FROM
            "data/raw/the_oscar_award.csv"
        WHERE
            canon_category = 'BEST PICTURE'
            AND ceremony = 96
    )
GROUP BY
    film
ORDER BY
    nomination_count DESC
LIMIT
    10;

-- create the master list with imdb_id
-- need to go year by year rather than the whole
SELECT
    film,
    year_film,
    year_ceremony,
    tmdb.imdb_id,
    tmdb.release_date,
    tmdb.genres,
    tmdb.runtime
from
    'data/raw/the_oscar_award.csv' as oscars
    JOIN 'data/raw/TMDB_all_movies.csv' as tmdb ON oscars.film = tmdb.title
where
    canon_category = 'BEST PICTURE'
    AND year_ceremony = 2025
    AND release_date > '2024-01-01'
    AND release_date < '2025-03-01'
    AND tmdb.imdb_id IS NOT NULL
ORDER BY
    tmdb.release_date DESC;

-- genre of all the nominations