from prefect import flow, task
from prefect.tasks import exponential_backoff
from pathlib import Path
from datetime import datetime, timedelta
from update_file_if_exists_in_gcs import update_file_if_exists_in_gcs
from prefect_gcp.cloud_storage import GcsBucket
from sodapy import Socrata
import pandas as pd
from utils.compute_hash import compute_hash

client = Socrata("data.sfgov.org", None)


@flow(log_prints=True)
def extract(offset: int):
    api_data = fetch_data_api(offset)
    updated_api_data = update_data(api_data)
    # dump_data_info_test(api_data_augmented)
    save_data_locally(updated_api_data)
    local_file_list = check_recently_modified_files()
    gcb_file_list = check_existing_files_in_gcb()
    update_file_if_exists_in_gcs(local_file_list, gcb_file_list)
    return local_file_list


@task(
    retries=4,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
)
def fetch_data_api(offset: int):
    records_count = client.get("wg3w-h783", select="count(*)")
    total_no_of_records = int(records_count[0]["count"])

    api_data = pd.DataFrame()

    while total_no_of_records != offset:
        results = client.get("wg3w-h783", offset=offset, limit=50000)
        results_df = pd.DataFrame.from_records(results)
        api_data = pd.concat([api_data, results_df])

        offset += len(results_df)

    with open("offset.txt", "w+") as f:
        f.write(str(offset))

    return api_data


@task()
def update_data(api_data):
    # Extract month and date from the incident_date column s

    col = pd.DatetimeIndex(api_data["incident_date"]).month.astype(str).str.zfill(2)
    api_data.insert(loc=4, column="incident_month", value=col)

    col = pd.DatetimeIndex(api_data["incident_date"]).day.astype(str).str.zfill(2)
    api_data.insert(loc=5, column="incident_day", value=col)

    api_data["incident_year"] = api_data["incident_year"].astype(str)

    # creating hash of the row and inserting it in end
    api_data["hash_key"] = api_data.apply(compute_hash, axis=1)

    return api_data


@task()
def save_data_locally(updated_api_data):
    # Create directory structure if it doesn't exist
    for year in updated_api_data["incident_year"].unique():
        year_dir = Path("data") / year
        year_dir.mkdir(parents=True, exist_ok=True)
        for month in updated_api_data[updated_api_data["incident_year"] == year][
            "incident_month"
        ].unique():
            month_dir = year_dir / month
            month_dir.mkdir(parents=True, exist_ok=True)

    # Save the DataFrame into year/month/day CSV files
    for _, row in updated_api_data.iterrows():
        file_path = (
            Path("data")
            / row["incident_year"]
            / row["incident_month"]
            / f"{row['incident_day']}.csv"
        )
        row.to_frame().T.to_csv(
            file_path, mode="a", header=not file_path.exists(), index=False
        )


@task()
def check_recently_modified_files():
    # Check for recently modified files

    # Specify the directory to search for files in
    directory_path = Path("data/")

    # Calculate the datetime range for today
    today = datetime.today()
    start_time = datetime(today.year, today.month, today.day)
    end_time = start_time + timedelta(days=1)

    # Loop through all files in the directory and get the paths of the ones modified today
    local_file_list = []
    for file_path in directory_path.glob("**/*"):
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if start_time <= mtime < end_time and "ipynb_checkpoints" not in str(
                file_path
            ):
                local_file_list.append(str(file_path))

    return local_file_list


@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
)
def check_existing_files_in_gcb():
    gcs_block = GcsBucket.load("gcp-bucket-block")

    # Load all blobs from gcs
    blob_list = gcs_block.list_blobs()
    gcb_file_list = [blob.name for blob in blob_list]
    return gcb_file_list
