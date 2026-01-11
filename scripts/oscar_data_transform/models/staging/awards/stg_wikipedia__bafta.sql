select
    film as title,
    lower(film) as title_lower,
    cast(split_part(year, '(', 1) as int) as ceremony_year,
    cast(
        regexp_replace(split_part(year, '(', 2), '[^0-9]', '', 'g') as int
    ) as ceremony,
    'best film' as award_category,
    is_winner as won_flag,
    case
        when is_winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
from
    read_csv_auto(
        '/Users/kaixuanchin/Code/oscars-datasets/data/scraped/bafta.csv'
    )
where
    year is not null