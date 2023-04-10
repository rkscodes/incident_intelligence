import shutil
from prefect import task
from pathlib import Path


@task
def remove_data_local():
    if Path("../../data/").is_dir():
        shutil.rmtree("../../data/")
