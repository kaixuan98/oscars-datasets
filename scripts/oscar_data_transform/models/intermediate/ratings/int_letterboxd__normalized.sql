select 
    letterboxd.title,
    letterboxd.title_lower,
    letterboxd.release_year,
    letterboxd.imdb_id,
    letterboxd.rating_value,
    letterboxd.rating_count,
    'letterboxd' as rating_source,
    'audience' as rating_group,
    5 as rating_scale 
from {{ref('int_letterboxd__patched')}} as letterboxd