{{
    config(
        materialized='table',
    )
}}

select * 
from {{ref('int_awards__unify')}}
