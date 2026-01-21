with enriched as (select 
    cc.*, 
    movies.imdb_id
from {{ref('stg_wikipedia__critics_choice')}} as cc
left join {{ref('stg_tmdb__movies')}} as movies 
    on cc.title_lower = movies.title_lower
    and cc.ceremony_year between movies.release_year - 2 and movies.release_year + 2
), 

removed as (
    select *
    from enriched
    where title_lower <> 'academyawardforbestpicture'
),

dedup as (
    select 
        *,
        row_number() over (partition by title_lower, ceremony_year
                            order by case when imdb_id is not null then 1 else 2 end) as rn 
    from removed
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