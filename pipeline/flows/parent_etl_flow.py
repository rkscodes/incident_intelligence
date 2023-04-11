from prefect import flow, task
from extract_flow import extract
from load_gcs_flow import load_gcs
from pathlib import Path
import shutil


@flow(log_prints=True)
def parent_etl_flow(offset: int = 0):
    local_file_list = extract(offset)
    load_gcs(local_file_list)
    remove_data_local()


@task()
def remove_data_local():
    if Path("data/").is_dir():
        shutil.rmtree("data/")


if __name__ == "__main__":
    # get offset
    offset = "0"
    try:
        with open("offset.txt", "r") as f:
            offset = f.readline()
    except FileNotFoundError:
        with open("offset.txt", "w+") as f:
            f.write("0")
    offset = int(offset)

    parent_etl_flow(offset)

# idea store offset value in .yaml file
# also store base of the project in that file
# make download path with respect to variable in this project
