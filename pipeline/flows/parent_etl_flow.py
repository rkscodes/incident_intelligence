import shutil
from pathlib import Path

from extract_flow import extract, total_no_of_records
from load_bigquery_flow import load_bigquery
from load_gcs_flow import load_gcs
from prefect import flow, task
from prefect.tasks import exponential_backoff
from prefect_gcp.cloud_storage import GcsBucket


@flow(log_prints=True)
def parent_etl_flow(offset: int = -1):
    # Get offset value from gcs
    if offset == -1:
        offset = get_offset()
        offset = int(offset)

    # sanity check
    if total_no_of_records() == offset:
        print("🚫 No new data to fetch")
        return
    say_hello()
    local_file_list = extract(offset)
    gcs_file_paths = load_gcs(local_file_list)
    load_bigquery(gcs_file_paths)
    remove_data_local()

@task()
def say_hello():
    print("Hello, this confirms it is pulling from github")
@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
)
def get_offset():
    """Downloads the offset file from the GCS bucket to the specified directory."""

    gcs_bucket: GcsBucket = GcsBucket.load("gcp-bucket-block")
    offset_dir: Path = Path("offset_dir")
    offset_file_name: str = "offset.txt"
    offset_file_path = offset_dir / Path(offset_file_name)

    offset_dir.mkdir(parents=True, exist_ok=True)

    # Check if the file exists in the bucket.
    if gcs_bucket.get_bucket().blob(offset_file_name).exists():
        # The file exists, so we can just download it.
        gcs_bucket.download_object_to_path(offset_file_name, offset_dir / offset_file_name)
    else:
        # The file does not exist, so we need to create it.
        with open(offset_dir / offset_file_name, "w") as file:
            file.write("0")
        file.close()
        gcs_bucket.upload_from_path(
            from_path=offset_dir / offset_file_name, to_path=offset_file_name
        )

    # Read the value

    with open(str(offset_file_path), "r") as file:
        offset = file.read()
    file.close()

    return offset


@task()
def remove_data_local():
    if Path("data/").is_dir():
        shutil.rmtree("data/")
    if Path("data-gcs/").is_dir():
        shutil.rmtree("data-gcs/")
    if Path("offset_dir/").is_dir():
        shutil.rmtree("offset_dir")


if __name__ == "__main__":
    # get offset
    # with open("config.json", "r") as config_file:
    #     config = json.load(config_file)

    # offset = config.get("offset")

    parent_etl_flow(-1)
