with enriched as(
    select 
        rotten_tomatoes.*,
        movies.imdb_id
    from {{ref('stg_rotten_tomatoes__ratings')}} as rotten_tomatoes
    left join {{ref('stg_tmdb__movies')}} as movies
        on rotten_tomatoes.title_lower=movies.title_lower
        and rotten_tomatoes.release_year between movies.release_year - 1 and movies.release_year + 1
), 

dedup as (
    select 
        *,
        row_number() over (partition by title_lower
                            order by case when imdb_id is not null then 1 else 2 end) as rn 
    from enriched
)

select 
    title,
    title_lower,
    release_year,
    rt_url as url,
    rt_tomatometer,
    rt_critics_count,
    rt_popcornmeter,
    rt_audiences_count,
    imdb_id
from dedup 
where rn =1 