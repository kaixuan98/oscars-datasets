with enriched as (
    select 
        bafta.*, 
        movies.imdb_id
    from {{ref('stg_wikipedia__bafta')}} as bafta
    left join {{ref('stg_tmdb__movies')}} as movies 
        on 
            bafta.title_lower = movies.title_lower
            and bafta.ceremony_year between movies.release_year - 2 and movies.release_year + 2
    where ceremony_year > 1990
), 

dedup as (
    select 
        *,
        row_number() over (partition by title_lower, ceremony_year
                            order by case when imdb_id is not null then 1 else 2 end) as rn 
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
    imdb_id
from dedup
where rn = 1
