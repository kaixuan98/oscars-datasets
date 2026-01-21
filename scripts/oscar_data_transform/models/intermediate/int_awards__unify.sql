with 
    bafta AS (
        select * from {{ref('int_bafta__enriched')}}
    ),

    cc AS (
        select * from {{ref('int_critics_choice__enriched')}}
    ),

    gg AS (
        select * from {{ref('int_golden_globes__enriched')}}
    ),

    oscars AS (
        select * from {{ref('int_oscars__enriched')}}
    ),

    sag as (
        select * from {{ref('int_sag__enriched')}}
    )

select * from bafta
union all
select * from cc
union all
select * from gg
union all
select * from oscars
union all
select * from sag
