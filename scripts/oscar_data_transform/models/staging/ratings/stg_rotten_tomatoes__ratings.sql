select
    film as title,
    REGEXP_REPLACE(lower(film), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    cast(year_film as integer) as release_year,
    rt_url,
    cast(rt_tomatometer as integer) as rt_tomatometer,
    cast(rt_critics_count as integer) as rt_critics_count,
    cast(rt_popcornmeter as integer) as rt_popcornmeter,
    cast(rt_audiences_count as integer) as rt_audiences_count
from
    {{source("scraped_data", 'rt-20260102')}}