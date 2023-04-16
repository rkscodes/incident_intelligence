import json

from prefect.blocks.system import JSON

with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Set the value of the JSON block
json_block_value = {
    "project_id": config.get("project_id"),
    "dataset_id": config.get("dataset_id"),
    "table_id": config.get("table_id"),
    "service_account_file_path": config.get("service_account_file_path"),
    "gcs_bucket_name": config.get("gcs_bucket_name"),
    "github_repo": config.get("github_repo"),
    "branch": config.get("branch"),
    "bucket": config.get("bucket"),
}

# Create the JSON block
json_block = JSON(value=json_block_value)
json_block.save("json-config")
