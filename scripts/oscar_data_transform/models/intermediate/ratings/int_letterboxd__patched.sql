select * from {{ref('int_letterboxd__enriched')}}
union all 
select * from {{ref('letterboxd_fixes')}}