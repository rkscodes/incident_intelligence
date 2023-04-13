import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from prefect import flow, task
from sodapy import Socrata
from utils.compute_hash import compute_hash

client = Socrata("data.sfgov.org", None)


@flow(log_prints=True)
def extract(offset: int):
    api_data = fetch_and_validate_api_data(offset)
    updated_api_data = update_data(api_data)
    save_data_locally(updated_api_data)
    local_file_list = check_recently_modified_files()
    return local_file_list


@flow(
    retries=4,
    retry_delay_seconds=2,
    log_prints=True,
)
def fetch_and_validate_api_data(offset: int):
    total_records = total_no_of_records()
    api_data = pd.DataFrame()

    while total_records != offset:
        results = client.get("wg3w-h783", offset=offset, limit=50000)
        results_df = pd.DataFrame.from_records(results)
        results_df = ensure_data_consitency(results_df)
        api_data = pd.concat([api_data, results_df])
        offset += len(results_df)

    update_offset(offset)

    return api_data


@task()
def update_offset(offset):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    config["offset"] = offset
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)


@task()
def ensure_data_consitency(results_df):
    results_df = results_df.rename(
        columns={
            ":@computed_region_n4xg_c4py": "computed_region_n4xg_c4py",
            ":@computed_region_nqbw_i6c3": "computed_region_nqbw_i6c3",
            ":@computed_region_jwn9_ihcz": "computed_region_jwn9_ihcz",
            ":@computed_region_26cr_cadq": "computed_region_26cr_cadq",
            ":@computed_region_qgnn_b9vv": "computed_region_qgnn_b9vv",
            ":@computed_region_h4ep_8xdi": "computed_region_h4ep_8xdi",
            ":@computed_region_jg9y_a9du": "computed_region_jg9y_a9du",
        }
    )

    # Create empty columns for any column name in columns_order that does not exist in the dataframe
    for col in COLUMNS_ORDER:
        if col not in results_df.columns:
            results_df[col] = pd.Series(dtype="object")

    return results_df


task()


def total_no_of_records() -> int:
    records_count = client.get("wg3w-h783", select="count(*)")
    total_records = int(records_count[0]["count"])
    return total_records


@task()
def update_data(api_data):
    # Extract month and date from the incident_date columns

    col = pd.DatetimeIndex(api_data["incident_date"]).month.astype(str).str.zfill(2)
    # api_data.insert(loc=4, column="incident_month", value=col)
    api_data["incident_month"] = col

    col = pd.DatetimeIndex(api_data["incident_date"]).day.astype(str).str.zfill(2)
    # api_data.insert(loc=5, column="incident_day", value=col)
    api_data["incident_day"] = col

    api_data["incident_year"] = api_data["incident_year"].astype(str)

    # creating hash of the row and inserting it in end
    api_data["hash_key"] = api_data.apply(compute_hash, axis=1)

    # remove symbols from name

    # Reorder the data in required state
    api_data = api_data[COLUMNS_ORDER]
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
        row.to_frame().T.to_csv(file_path, mode="a", header=not file_path.exists(), index=False)


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
            if start_time <= mtime < end_time and "ipynb_checkpoints" not in str(file_path):
                local_file_list.append(file_path)

    return local_file_list


COLUMNS_ORDER = [
    "incident_datetime",
    "incident_date",
    "incident_time",
    "incident_year",
    "incident_month",
    "incident_day",
    "incident_day_of_week",
    "report_datetime",
    "row_id",
    "incident_id",
    "incident_number",
    "report_type_code",
    "report_type_description",
    "incident_code",
    "incident_category",
    "incident_subcategory",
    "incident_description",
    "resolution",
    "police_district",
    "filed_online",
    "cad_number",
    "intersection",
    "cnn",
    "analysis_neighborhood",
    "supervisor_district",
    "supervisor_district_2012",
    "latitude",
    "longitude",
    "point",
    "computed_region_jwn9_ihcz",
    "computed_region_26cr_cadq",
    "computed_region_qgnn_b9vv",
    "computed_region_n4xg_c4py",
    "computed_region_nqbw_i6c3",
    "computed_region_h4ep_8xdi",
    "computed_region_jg9y_a9du",
    "hash_key",
]
