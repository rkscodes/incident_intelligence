from datetime import datetime
from pathlib import Path
from typing import List

from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from utils.renamed_file_name import renamed_file_name


@flow(log_prints=True)
def load_gcs(files: List) -> Path:
    gcs_block = GcsBucket.load("gcp-bucket-block")
    gcs_file_path = []

    for path in files:
        upload_path = to_path(path=path)
        gcs_block.upload_from_path(from_path=path, to_path=upload_path)
        gcs_file_path.append(upload_path)

    return gcs_file_path


def to_path(path: Path) -> Path:
    today = datetime.today()
    year, month, day = (
        str(today.year),
        str(today.month).zfill(2),
        str(today.day).zfill(2),
    )
    path = Path(year) / Path(month) / Path(day) / renamed_file_name(path)
    return path
