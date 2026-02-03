with oscars as (
    select
        o.*,
        coalesce(o_override.imdb_id, null) as override_imdb_id
    from {{ ref('stg_kaggle__oscars') }} o
    left join {{ ref('film_identity_overwrite') }} o_override
        on o_override.source_system='oscars'
        and o_override.source_title_lower=o.title_lower
        and o_override.source_year = o.ceremony_year
    where ceremony_year > 1990 and award_category = 'best picture'

),

merged as (
    select
        tmdb.*
    from oscars
    left join {{ ref('stg_tmdb__ratings') }} tmdb
        on (oscars.override_imdb_id is not null and oscars.override_imdb_id = tmdb.imdb_id)
        or (oscars.override_imdb_id is null 
            and oscars.title_lower = tmdb.title_lower
            and oscars.ceremony_year between tmdb.release_year - 2 and tmdb.release_year + 2)
),

dedup as (
    select 
        *,
        row_number() over (partition by title_lower
                            order by case when imdb_id is not null and rating_count > 500 then 1 else 2 end) as rn 
    from merged
)


select 
    title,
    title_lower,
    release_year,
    imdb_id,
    rating as rating_value,
    rating_count,
    'tmdb' as rating_source,
    'audience' as rating_group,
    100 as rating_scale
from dedup
where rn=1 

