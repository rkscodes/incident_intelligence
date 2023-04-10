from prefect import flow
from prefect_gcp.cloud_storage import GcsBucket
from typing import List
from utils.renamed_file_name import renamed_file_name


@flow(log_prints=True)
def load_gcs(files: List):
    gcs_block = GcsBucket.load("gcp-bucket-block")

    for path in files:
        from_path = path
        to_path = renamed_file_name(path)
        gcs_block.upload_from_path(from_path=from_path, to_path=to_path)
