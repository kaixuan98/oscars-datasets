select 
    golden_globes.*,
    movies.imdb_id
from {{ ref('stg_golden_globes__awards') }} as golden_globes
left join {{ ref('stg_tmdb__movies') }} as movies
    on
        golden_globes.title_lower = movies.title_lower
        and golden_globes.ceremony_year between movies.release_year - 1 and movies.release_year + 1
        and movies.budget > 0 and movies.runtime >= 90