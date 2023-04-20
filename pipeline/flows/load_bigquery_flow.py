from pathlib import Path

import pandas as pd
from google.cloud import bigquery
from prefect import flow, task
from prefect.blocks.system import JSON
from prefect.tasks import exponential_backoff
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@flow(log_prints=True)
def load_bigquery(gcs_file_paths):
    path_list = extract_from_gcs(gcs_file_paths=gcs_file_paths)
    gcs_data_all = transform(path_list)
    upload_gbq(gcs_data_all)


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
def transform(path_list):
    li = []
    for path in path_list:
        df = pd.read_csv(path, index_col=None, header=0)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv("data-gcs/data-all.csv", index=False)
    # row.to_frame().T.to_csv(file_path, mode="a", header=not file_path.exists(), index=False)
    return Path("data-gcs/data-all.csv")


@task()
def upload_gbq(gcs_data_all):
    # Getting required config from json block
    json_block = JSON.load("json-config")
    dataset_id = json_block.value["dataset_id"]
    table_id = json_block.value["table_id"]

    gcp_credentials_block = GcpCredentials.load("gcp-credential-block")
    credentials = gcp_credentials_block.get_credentials_from_service_account()

    # setting google client
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    dataset = client.dataset(dataset_id)
    table = dataset.table(table_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    with open(gcs_data_all.resolve(), "rb") as file:
        load_job = client.load_table_from_file(
            file,
            table,
            job_config=job_config,  # omit schema parameter
        )
    load_job.result()
