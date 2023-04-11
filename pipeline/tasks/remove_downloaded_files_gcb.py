from prefect import task
from pathlib import Path
import shutil


@task
def remove_downloaded_files_gcb(dir: str):
    if Path(dir).is_dir():
        shutil.rmtree(dir)
