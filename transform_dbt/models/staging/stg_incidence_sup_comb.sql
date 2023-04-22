select a.*, b.*

from {{ ref("stg_incidence_data") }} as a
join{{ ref("stg_sup_dist") }} as b on a.supervisor_district = b.supervisor_district_no
