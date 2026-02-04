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
    (rating_value/ rating_scale) * 100 as rating_normalized
from {{ref('int_ratings__canonical_id')}}
