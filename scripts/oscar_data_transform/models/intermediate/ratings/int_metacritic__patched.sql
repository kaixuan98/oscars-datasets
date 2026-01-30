select * from {{ref('int_metacritic__enriched')}}
union all 
select * from {{ref('metacritic_fixes')}}