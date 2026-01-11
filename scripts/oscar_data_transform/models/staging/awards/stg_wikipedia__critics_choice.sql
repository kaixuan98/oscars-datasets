select
    film as title,
    lower(film) as title_lower,
    year as ceremony_year,
    'critics choice' as award_body,
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