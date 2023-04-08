from pathlib import Path
import pandas as pd 
from sodapy import Socrata
from datetime import datetime, timedelta
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from typing import List
import shutil
import extract_flow
import load_gcs_flow
import update_gcb_flow

client = Socrata("data.sfgov.org", None)





@flow(log_prints=True)
def parent_etl_flow(offset: int = 0):
    local_file_list = extract(offset)
    load_gcs_flow(local_file_list)
    remove_data_local()


if __name__ == "__main__":
    # get offset 
    offset = '0'
    try:
        with open("offset.txt", "r") as f:
            offset = f.readline()
    except FileNotFoundError:
        with open("offset.txt", "w+") as f:
            f.write("0")     
    offset = int(offset)
     
    etl_flow(offset=714500)

# idea store offset value in .yaml file 
# also store base of the project in that file
# make download path with respect to variable in this project 