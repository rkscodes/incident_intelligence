from prefect import task
from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket
from typing import List


@task
def download_common_files_gcb(common_files: List):
    for files in common_files:
        to_path_dir = Path("temp") / Path(files).parent
        to_path_dir.mkdir(parents=True, exist_ok=True)
        # to_path_name = Path(to_path_dir + '/' + str(Path(files).name))
        to_path_name = to_path_dir / Path(files).name

        print("Downloading to path", to_path_name)

        gcs_block = GcsBucket.load("gcp-bucket-block")
        gcs_block.download_object_to_path(from_path=files, to_path=to_path_name)
