select
    movies.*,
    distributors.distributor as distributor_name
from
    {{ ref('stg_tmdb__movies') }} as movies
left join {{ ref('stg_rotten_tomatoes__distributors') }} as distributors
    on
        movies.title_lower = distributors.title_lower
        and movies.release_year between distributors.release_year - 1
        and distributors.release_year + 1