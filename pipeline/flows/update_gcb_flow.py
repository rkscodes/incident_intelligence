from prefect import flow
from typing import List
import pandas as pd
from pipeline.tasks.common_files_names import common_files_names
from pipeline.tasks.download_common_files_gcb import download_common_files_gcb
from pipeline.tasks.remove_downloaded_files_gcb import remove_downloaded_files_gcb


@flow(log_prints=True)
def update_gcb_file_if_already_exists(local_file_list: List, gcb_file_list: List):
    common_files = common_files_names(local_file_list, gcb_file_list)
    download_common_files_gcb(common_files)

    # joining the data
    for files in common_files:
        new_df = pd.read_csv(f"../../{files}")
        gcs_df = pd.read_csv(f"temp/{files}")
        df = pd.concat([gcs_df, new_df], axis=0)
        df.to_csv(f"../../{files}", index=False)

    remove_downloaded_files_gcb("temp")
