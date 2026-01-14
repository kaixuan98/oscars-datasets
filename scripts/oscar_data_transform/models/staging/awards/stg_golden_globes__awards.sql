select
    title,
    lower(title) as title_lower,
    year as ceremony_year,
    lower(category) as award_category,
    'golden globe' as award_body,
    is_winner as won_flag,
    case
        when is_winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
from
    {{source('scraped_data', 'golden_globes')}}