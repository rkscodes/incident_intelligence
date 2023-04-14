import json
import shutil
from pathlib import Path

from extract_flow import extract, total_no_of_records
from load_bigquery_flow import load_bigquery
from load_gcs_flow import load_gcs
from prefect import flow, task


@flow(log_prints=True)
def parent_etl_flow(offset: int = 0):
    # sanity check
    if total_no_of_records() == offset:
        print("No new data to fetch")
        return

    local_file_list = extract(offset)
    gcs_file_paths = load_gcs(local_file_list)
    load_bigquery(gcs_file_paths)
    remove_data_local()


@task()
def remove_data_local():
    if Path("data/").is_dir():
        shutil.rmtree("data/")
    if Path("data-gcs/").is_dir():
        shutil.rmtree("data-gcs/")


if __name__ == "__main__":
    # get offset
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    offset = config.get("offset")

    parent_etl_flow(offset)
