with raw_clean as (
    select
        title,
        regexp_replace(lower(title), '\s*\(\d{4}\)$', '') as title_no_year,
        year as ceremony_year,
        lower(category) as award_category,
        is_winner as won_flag
    from {{ source('scraped_data', 'golden_globes') }}
),

normalized as (
    select
        title,
        trim(
            case
                when title_no_year like '%, the' then 'the ' || split_part(title_no_year, ',', 1)
                when title_no_year like '%, a' then 'a ' || split_part(title_no_year, ',', 1)
                when title_no_year like '%, an' then 'an ' || split_part(title_no_year, ',', 1)
                else title_no_year
            end
        ) as title_lower_normalized,
        ceremony_year,
        award_category,
        'golden globe' as award_body,
        won_flag,
        case
            when won_flag = true then 'WON'
            else 'NOMINATED'
        end as award_result
    from raw_clean
)

select 
    title,
    regexp_replace(title_lower_normalized, '[^a-zA-Z0-9]', '', 'g') as title_lower,
    ceremony_year, 
    award_category,
    award_body,
    won_flag,
    award_result
from normalized