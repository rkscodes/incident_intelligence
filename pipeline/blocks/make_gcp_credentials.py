import json
from pathlib import Path

from prefect_gcp import GcpCredentials

# replace this PLACEHOLDER dict with your own service account info
with open("config.json", "r") as config_file:
    config = json.load(config_file)

service_account_file = config.get("service_account_file_path")

GcpCredentials(service_account_file=service_account_file).save("gcp-credential-block")
