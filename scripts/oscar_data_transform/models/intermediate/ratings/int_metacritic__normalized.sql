select 
    title,
    title_lower,
    release_year,
    url,
    mc_metascore as rating_value,
    mc_metascore_count as rating_count,
    'critic' as rating_group,
    100 as rating_scale,
    'metacritic'  as rating_source
from {{ref('int_metacritic__patched')}}
union all 
select 
    title,
    title_lower,
    release_year,
    url,
    mc_users_score as rating_value,
    mc_users_count as rating_count,
    'audience' as rating_group,
    10 as rating_scale,
    'metacritic'  as rating_source
from {{ref('int_metacritic__patched')}}