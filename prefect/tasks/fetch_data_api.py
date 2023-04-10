from prefect import task

from utils.client import client
import pandas as pd


@task()
def fetch_data_api(offset: int):
    records_count = client.get("wg3w-h783", select="count(*)")
    total_no_of_records = int(records_count[0]["count"])

    api_data = pd.DataFrame()

    while total_no_of_records != offset:
        results = client.get("wg3w-h783", offset=offset, limit=50000)
        results_df = pd.DataFrame.from_records(results)
        api_data = pd.concat([api_data, results_df])

        offset += len(results_df)
        offset

    with open("offset.txt", "w+") as f:
        f.write(str(offset))

    return api_data
