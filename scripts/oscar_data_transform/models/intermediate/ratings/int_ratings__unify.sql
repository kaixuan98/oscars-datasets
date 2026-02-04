with
    letterboxd as (
        select * from {{ref('int_letterboxd__normalized')}}
    ),
    metacritic as (
        select * from {{ref('int_metacritic__normalized')}}
    ),
    rt as (
        select * from {{ref('int_rotten_tomatoes__normalized')}}
    ),
    imdb as (
        select * from {{ref('int_imdb__normalized')}}
    ),
    tmdb as (
        select * from {{ref('int_tmdb__normalized')}}
    )

select * from letterboxd
union all
select * from metacritic
union all 
select * from rt
union all
select * from imdb
union all
select * from tmdb

