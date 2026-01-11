select
    title,
    lower(title) as title_lower,
    year as release_year,
    lower(category) as award_category,
    'golden_globe' as award_body,
    is_winner as won_flag,
    case
        when is_winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
from
    read_csv_auto(
        '/Users/kaixuanchin/Code/oscars-datasets/data/scraped/golden_globes.csv'
    )