from prefect.blocks.system import JSON
from prefect_dbt.cli.configs import BigQueryTargetConfigs
from prefect_gcp.credentials import GcpCredentials

json_block = JSON.load("json-config")
credentials = GcpCredentials.load("gcp-credential-block")


target_config = BigQueryTargetConfigs(
    schema=json_block.value["dataset_id"],
    credentials=credentials,
    threads=4,
    project=json_block.value["project_id"],
).save("dbt-cli-bigquery-target-block")
