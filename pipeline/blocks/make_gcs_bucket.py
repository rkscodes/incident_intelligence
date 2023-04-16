from prefect.blocks.system import JSON
from prefect_gcp import GcpCredentials, GcsBucket

json_block = JSON.load("json-config")

bucket = json_block.value["bucket"]

GcsBucket(bucket=bucket, gcp_credentials=GcpCredentials.load("gcp-credential-block")).save(
    "gcp-bucket-block"
)
