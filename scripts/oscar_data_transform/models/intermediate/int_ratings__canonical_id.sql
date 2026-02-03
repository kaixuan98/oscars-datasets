with imdb_preferred as (
    select
        title_lower,
        max(imdb_id) as canonical_imdb_id
    from {{ ref('int_ratings__unify') }}
    where rating_source = 'imdb'
      and imdb_id is not null
    group by title_lower
), 
imdb_counts as (
    select
        title_lower,
        imdb_id,
        count(*) as cnt
    from {{ ref('int_ratings__unify') }}
    where imdb_id is not null
    group by title_lower, imdb_id
), 
fallback as (
    select
        title_lower,
        imdb_id as canonical_imdb_id
    from (
        select
            *,
            row_number() over (
                partition by title_lower
                order by cnt desc
            ) as rn
        from imdb_counts
    ) t
    where rn = 1
), 
canonical_imdb as (
    select
        coalesce(i.title_lower, f.title_lower) as title_lower,
        coalesce(i.canonical_imdb_id, f.canonical_imdb_id) as canonical_imdb_id
    from imdb_preferred i
    full outer join fallback f
        on i.title_lower = f.title_lower
)


select
    r.*,
    r.imdb_id as original_imdb_id,
    c.canonical_imdb_id
from {{ ref('int_ratings__unify') }} r
left join canonical_imdb c
    on r.title_lower = c.title_lower