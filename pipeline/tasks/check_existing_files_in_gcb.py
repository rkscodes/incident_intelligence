from prefect import task
from prefect.tasks import exponential_backoff
from prefect_gcp.cloud_storage import GcsBucket


@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
)
def check_existing_files_in_gcb():
    gcs_block = GcsBucket.load("gcp-bucket-block")

    # Load all blobs from gcs
    blob_list = gcs_block.list_blobs()
    gcb_file_list = [blob.name for blob in blob_list]
    return gcb_file_list
