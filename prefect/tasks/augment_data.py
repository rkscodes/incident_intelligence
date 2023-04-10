from prefect import task
import pandas as pd


@task()
def augment_data(api_data):
    # Extract month and date from the incident_date column s

    col = pd.DatetimeIndex(api_data["incident_date"]).month.astype(str).str.zfill(2)
    api_data.insert(loc=4, column="incident_month", value=col)

    col = pd.DatetimeIndex(api_data["incident_date"]).day.astype(str).str.zfill(2)
    api_data.insert(loc=5, column="incident_day", value=col)

    api_data["incident_year"] = api_data["incident_year"].astype(str)

    return api_data
