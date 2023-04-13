from prefect_gcp import GcpCredentials, GcsBucket

bucket = "incident_data_lake_affable-tangent-382517"

GcsBucket(bucket=bucket, gcp_credentials=GcpCredentials.load("gcp-credential-block")).save(
    "gcp-bucket-block"
)
