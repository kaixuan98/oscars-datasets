select
    film as title,
    REGEXP_REPLACE(lower(film), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    cast(year_film as integer) as release_year,
    mc_url,
    cast(mc_metascore as integer) as mc_metascore,
    cast(mc_metascore_count as integer) as mc_metascore_count,
    cast(mc_users_score as double) as mc_users_score,
    cast(mc_users_count as integer) as mc_users_count

from
    {{source("scraped_data", 'mc_20260102')}}