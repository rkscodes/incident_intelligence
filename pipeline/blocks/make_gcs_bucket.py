import json

from prefect_gcp import GcpCredentials, GcsBucket

with open("config.json", "r") as config_file:
    config = json.load(config_file)

bucket = config.get("gcs_bucket_name")

GcsBucket(bucket=bucket, gcp_credentials=GcpCredentials.load("gcp-credential-block")).save(
    "gcp-bucket-block"
)
