from prefect import flow, task
import pandas as pd
import hashlib


@flow()
def augment_data(api_data):
    # Extract month and date from the incident_date column s

    col = pd.DatetimeIndex(api_data["incident_date"]).month.astype(str).str.zfill(2)
    api_data.insert(loc=4, column="incident_month", value=col)

    col = pd.DatetimeIndex(api_data["incident_date"]).day.astype(str).str.zfill(2)
    api_data.insert(loc=5, column="incident_day", value=col)

    api_data["incident_year"] = api_data["incident_year"].astype(str)

    # creating hash of the row and inserting it in end
    api_data["hash"] = api_data.apply(compute_hash, axis=1)

    return api_data


@task()
def compute_hash(row):
    row_str = " ".join([str(val) for val in row.values])

    hash_value = hashlib.md5(row_str.encode()).hexdigest()
    return hash_value
