-- {{config(materialized="table")}}
with
    ingest_data as (
        -- deduplication step 
        select *, row_number() over (partition by hash_key) as rn
        from {{ source("default", "raw_ingest") }}
    )
select
    cast(incident_datetime as timestamp) as incident_datetime,
    cast(incident_date as date) as incident_date,
    cast(concat(incident_time, ':00') as time) as incident_time,
    cast(incident_year as int64) as incident_year,
    cast(incident_month as int64) as incident_month,
    cast({{ get_month_name("incident_month") }} as string) as incident_month_name,
    cast(incident_day as int64) as incident_day,
    cast(incident_day_of_week as string) as incident_day_of_week,
    cast(report_datetime as timestamp) as report_datetime,
    cast(row_id as int64) as row_id,
    cast(incident_id as int64) as incident_id,
    cast(incident_number as int64) as incident_number,
    cast(report_type_code as string) as report_type_code,
    cast(report_type_description as string) as report_type_description,
    cast(incident_code as int64) as incident_code,
    cast(incident_category as string) as incident_category,
    cast(incident_subcategory as string) as incident_subcategory,
    cast(incident_description as string) as incident_description,
    cast(resolution as string) as resolution,
    cast(police_district as string) as police_district,
    ifnull(cast(filed_online as string), 'unspecified') as filed_online,
    cast(cad_number as float64) as cad_number,
    cast(intersection as string) as intersection,
    cast(cnn as int64) as cnn,
    cast(analysis_neighborhood as string) as analysis_neighborhood,
    cast(supervisor_district as int64) as supervisor_district,
    cast(latitude as float64) as latitude,
    cast(longitude as float64) as longitude,
    cast(hash_key as string) as original_table_hash_key

from ingest_data
where rn = 1

-- dbt build -m <model_name> --var 'is_test_run: false'
{% if var("is_test_run", default=false) %} limit 100 {% endif %}
