select 
    letterboxd.*,
    'letterboxd' as rating_source,
    'audience' as rating_group,
    5 as rating_scale 
from {{ref('int_letterboxd__patched')}} as letterboxd