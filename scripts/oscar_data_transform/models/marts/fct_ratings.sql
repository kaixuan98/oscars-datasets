{{
    config(
        materialized='table',
    )
}}

select 
    canonical_imdb_id as imdb_id,
    title,
    title_lower,
    release_year,
    rating_source,
    rating_group,
    rating_value,
    rating_count,
    (rating_value/ rating_scale) * 100 as rating_normalized,
    ((rating_value/rating_scale ) * 100) * rating_count as weighted_score
from {{ref('int_ratings__canonical_id')}}
