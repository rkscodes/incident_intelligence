import json
from pathlib import Path

from google.cloud import bigquery
from prefect import flow, task
from prefect.tasks import exponential_backoff
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@flow(log_prints=True)
def load_bigquery(gcs_file_paths):
    path_list = extract_from_gcs(gcs_file_paths=gcs_file_paths)
    upload_gbq(path_list)


@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
)
def extract_from_gcs(gcs_file_paths: Path):
    """Download data from gcs"""
    gcs_block = GcsBucket.load("gcp-bucket-block")
    path_list = []

    for gcs_path in gcs_file_paths:
        gcs_block.get_directory(from_path=gcs_path, local_path=f"data-gcs/")
        path_list.append(Path(f"data-gcs/{gcs_path}"))
    return path_list


@task()
def upload_gbq(path_list):
    # reading required variables
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    dataset_id = config.get("dataset_id")
    table_id = config.get("table_id")

    gcp_credentials_block = GcpCredentials.load("gcp-credential-block")
    credentials = gcp_credentials_block.get_credentials_from_service_account()

    # setting google client
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    dataset = client.dataset(dataset_id)
    table = dataset.table(table_id)

    schema = [
        bigquery.SchemaField("incident_datetime", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("incident_date", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("incident_time", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("incident_year", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("incident_month", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("incident_day", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("incident_day_of_week", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("report_datetime", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("row_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("incident_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("incident_number", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("report_type_code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("report_type_description", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("incident_code", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("incident_category", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("incident_subcategory", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("incident_description", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("resolution", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("police_district", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("filed_online", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("cad_number", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("intersection", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("cnn", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("analysis_neighborhood", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("supervisor_district", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("supervisor_district_2012", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("latitude", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("longitude", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("point", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_jwn9_ihcz", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_26cr_cadq", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_qgnn_b9vv", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_n4xg_c4py", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_nqbw_i6c3", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_h4ep_8xdi", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("computed_region_jg9y_a9du", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("hash_key", "STRING", mode="REQUIRED"),
    ]

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        schema=schema,
    )
    for path in path_list:
        with open(path.resolve(), "rb") as file:
            load_job = client.load_table_from_file(
                file,
                table,
                job_config=job_config,  # omit schema parameter
            )
        load_job.result()
        print(f"INSERTED {path} in {table_id}")
