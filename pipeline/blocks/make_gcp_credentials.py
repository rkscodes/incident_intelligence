from prefect.blocks.system import JSON
from prefect_gcp import GcpCredentials

json_block = JSON.load("json-config")

service_account_file = json_block.value["service_account_file_path"]

GcpCredentials(service_account_file=service_account_file).save("gcp-credential-block")
