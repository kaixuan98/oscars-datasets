select 
    title,
    title_lower,
    release_year,
    url,
    rt_tomatometer as rating_value,
    rt_critics_count as rating_count,
    'critic' as rating_group,
    100 as rating_scale,
    'rotten_tomatoes' as rating_source
from {{ref('int_rotten_tomatoes__enriched')}}
union all 
select 
    title,
    title_lower,
    release_year,
    url,
    rt_popcornmeter as rating_value,
    rt_audiences_count as rating_count,
    'audience' as rating_group,
    100 as rating_scale,
    'rotten_tomatoes' as rating_source
from {{ref('int_rotten_tomatoes__enriched')}}