select 
    title,
    title_lower,
    release_year,
    imdb_id,
    rt_tomatometer as rating_value,
    rt_critics_count as rating_count,
    'rotten_tomatoes' as rating_source,
    'critic' as rating_group,
    100 as rating_scale
from {{ref('int_rotten_tomatoes__enriched')}}
union all 
select 
    title,
    title_lower,
    release_year,
    imdb_id,
    rt_popcornmeter as rating_value,
    rt_audiences_count as rating_count,
    'rotten_tomatoes' as rating_source,
    'audience' as rating_group,
    100 as rating_scale
from {{ref('int_rotten_tomatoes__enriched')}}