from prefect import task
from datetime import datetime, timedelta
from pathlib import Path


@task()
def check_recently_modified_files():
    # Check for recently modified files

    # Specify the directory to search for files in
    directory_path = Path("../../data/")

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
