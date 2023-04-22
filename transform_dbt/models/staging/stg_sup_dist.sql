select
    sup_name as supervisor_name,
    sup_dist as supervisor_district_no,
    sup_dist_name as supervisor_district_name

from {{ ref("sup_dist_lookup") }}
