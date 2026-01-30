with enriched as(
    select 
        metacritic.*,
        movies.imdb_id
    from {{ref('stg_metacritic__ratings')}} as metacritic
    left join {{ref('stg_tmdb__movies')}} as movies
        on metacritic.title_lower like movies.title_lower || '%'
        and metacritic.release_year between movies.release_year - 1 and movies.release_year + 1
), 

dedup as (
    select 
        *,
        row_number() over (partition by title_lower, release_year
                            order by case when imdb_id is not null then 1 else 2 end) as rn 
    from enriched
)

select 
    title,
    title_lower,
    release_year,
    mc_url as url,
    mc_metascore,
    mc_metascore_count,
    mc_users_score,
    mc_users_count,
    imdb_id
from dedup 
where rn =1 