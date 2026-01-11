select
    film as title,
    lower(film) as title_lower,
    year as release_year,
    'best picture' as award_category,
    is_winner as won_flag,
    case
        when is_winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
from
    read_csv_auto(
        '/Users/kaixuanchin/Code/oscars-datasets/data/scraped/critics_choice.csv'
    )