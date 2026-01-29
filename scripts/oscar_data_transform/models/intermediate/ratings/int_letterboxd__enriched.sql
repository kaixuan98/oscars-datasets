with enriched as(
    select 
        letterboxd.*,
        movies.imdb_id
    from {{ref('stg_letterboxd__ratings')}} as letterboxd
    left join {{ref('stg_tmdb__movies')}} as movies
        on letterboxd.title_lower like movies.title_lower || '%'
        and letterboxd.release_year between movies.release_year - 1 and movies.release_year + 1
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
    lb_url,
    rating_value,
    rating_count,
    watched_count,
    liked_count,
    imdb_id
from dedup 
where rn =1 
