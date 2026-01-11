SELECT
    film as title,
    lower(film) as title_lower,
    year_film as release_year,
    year_ceremony,
    ceremony,
    name,
    winner as won_flag,
    canon_category as award_category,
    'oscars' as award_body,
    case
        when winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
FROM
    read_csv_auto(
        '/Users/kaixuanchin/Code/oscars-datasets/data/raw/the_oscar_award.csv'
    )