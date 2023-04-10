from prefect import task
from prefect_gcp.cloud_storage import GcsBucket


@task
def check_existing_files_in_gcb():
    gcs_block = GcsBucket.load("gcp-bucket-block")

    # Load all blobs from gcs
    blob_list = gcs_block.list_blobs()
    gcb_file_list = [blob.name for blob in blob_list]
    return gcb_file_list
