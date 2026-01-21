SELECT
    film as title,
    REGEXP_REPLACE(lower(film), '[^a-zA-Z0-9]', '', 'g') as title_lower,
    year_film as release_year,
    year_ceremony as ceremony_year,
    name,
    winner as won_flag,
    lower(canon_category) as award_category,
    'oscars' as award_body,
    case
        when winner = true then 'WON'
        else 'NOMINATED'
    end as award_result
FROM
    {{source("raw_data", 'the_oscar_award')}}