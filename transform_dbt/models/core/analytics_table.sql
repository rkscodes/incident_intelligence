{{ config(materialized="table") }}

select
    incident_datetime,
    incident_date,
    incident_time,
    incident_year,
    incident_month,
    incident_month_name,
    incident_day,
    incident_day_of_week,
    report_datetime,
    incident_id,
    incident_number,
    report_type_code,
    report_type_description,
    incident_code,
    incident_category,
    incident_subcategory,
    incident_description,
    resolution,
    police_district,
    filed_online,
    cad_number,
    intersection,
    cnn,
    analysis_neighborhood,
    supervisor_district,
    supervisor_district_2012,
    latitude,
    longitude,
    original_table_hash_key

from {{ ref("stg_incidence_data") }}