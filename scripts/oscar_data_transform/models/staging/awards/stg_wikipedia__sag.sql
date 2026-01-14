select
    film as title,
    lower(film) as title_lower,
    cast(split_part(year, '(', 1) as int) + 1 as ceremony_year,
    'sag' as award_body,
    'outstanding performance by a cast in a motion picture' as award_category,
    is_winner as won_flag,
    case
        when is_winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
from
    {{source('scraped_data', 'screen_actor_guild')}}