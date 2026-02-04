{{
    config(
        materialized="table",
        unique_key="imdb_id"
    )
}}


select 
    imdb_id, 
    title, 
    title_lower,
    release_date,
    release_year,
    revenue,
    runtime,
    budget,
    original_language,
    overview,
    genres,
    production_companies,
    cast_members,
    director,
    director_of_photography,
    writers,
    producers,
    poster_path,
    distributor_name as distributor 
from {{ref('int_movies__enriched')}}