with enriched as (
    select 
        oscars.*,
        overwritten.imdb_id as overwrite_imdb_id,
        movies.imdb_id as imdb_id,
        movies.release_year,
        movies.runtime,
        movies.director,
        movies.writers,
        movies.producers
    from {{ref('stg_kaggle__oscars')}} as oscars
    left join {{ref('film_identity_overwrite')}} as overwritten
        on overwritten.source_system = 'oscars'
        and overwritten.source_title_lower = oscars.title_lower
        and overwritten.source_year = oscars.ceremony_year
    left join {{ref('stg_tmdb__movies')}} as movies 
        on 
            oscars.title_lower=movies.title_lower
            and oscars.ceremony_year between movies.release_year - 2 and movies.release_year + 2
            and movies.runtime > 80
            and movies.director IS NOT NULL
            and movies.writers IS NOT NULL
            and movies.producers IS NOT NULL
    where ceremony_year > 1990 and award_category = 'best picture'
), 

ranked as (
    select
        *,
        row_number() over (
            partition by title_lower, ceremony_year
            order by
                -- Priority ranking
                case 
                    when overwrite_imdb_id is not null then 1  -- manual override wins
                    when imdb_id is not null
                         and director is not null
                         and writers is not null
                         and producers is not null then 2  -- complete TMDB
                    when imdb_id is not null then 3      -- partial TMDB
                    else 99                                   -- fallback
                end,
                abs(coalesce(release_year, ceremony_year) - ceremony_year),  -- tie-breaker: closest year
                runtime desc  -- tie-breaker: longer movie preferred
        ) as rn
    from enriched
)

select 
    title,
    title_lower, 
    ceremony_year, 
    award_body, 
    award_category,
    won_flag,
    award_result, 
    coalesce(overwrite_imdb_id, imdb_id) as imdb_id
from ranked
where rn = 1