with base as (
    select *
    from {{ ref('int_ratings__unify') }}
),

patched as (
    select
        base.title,
        base.title_lower,
        base.release_year,
        base.rating_source,
        base.rating_group,
        base.rating_value,
        base.rating_count,
        base.rating_scale,
        coalesce(
            overwritten.imdb_id,
            base.imdb_id
        ) as imdb_id

    from base
    left join {{ ref('film_identity_overwrite') }} overwritten
        on base.title_lower = overwritten.source_title_lower
)

select *
from patched
