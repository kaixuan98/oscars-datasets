select
    film as title,
    lower(film) as title_lower,
    year as ceremony_year,
    'venice' as festival_name,
    'golden lion' as festival_prize
from
    read_csv_auto(
        '/Users/kaixuanchin/Code/oscars-datasets/data/scraped/venice_golden_lion.csv'
    )
where
    title_lower not like '[%'