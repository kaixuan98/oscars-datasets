select
    film as title,
    lower(film) as title_lower,
    year as ceremony_year,
    'cannes' as festival_name,
    'palme d''or' as festival_prize
from
    read_csv_auto(
        '/Users/kaixuanchin/Code/oscars-datasets/data/scraped/cannes_palme_d_or.csv'
    )