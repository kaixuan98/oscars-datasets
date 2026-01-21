with enriched as (
    select 
        oscars.*, 
        movies.imdb_id
    from {{ref('stg_kaggle__oscars')}} as oscars
    left join {{ref('stg_tmdb__movies')}} as movies 
        on 
            oscars.title_lower like movies.title_lower ||'%'
            and oscars.ceremony_year between movies.release_year - 2 and movies.release_year + 2
    where ceremony_year > 1990 and award_category = 'best picture'
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