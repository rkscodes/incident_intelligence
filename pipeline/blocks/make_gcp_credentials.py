import json

from prefect.blocks.system import JSON
from prefect_gcp import GcpCredentials

json_block = JSON.load("json-config")

service_account_file = json_block.value["service_account_file_path"]

# This way is required so that you would be independent of file location ex in docker, coudln't find location
with open(service_account_file, "r") as file:
    json_content = json.load(file)

service_account_info = {
    "type": json_content["type"],
    "project_id": json_content["project_id"],
    "private_key_id": json_content["private_key_id"],
    "private_key": json_content["private_key"],
    "client_email": json_content["client_email"],
    "client_id": json_content["client_id"],
    "auth_uri": json_content["auth_uri"],
    "token_uri": json_content["token_uri"],
    "auth_provider_x509_cert_url": json_content["auth_provider_x509_cert_url"],
    "client_x509_cert_url": json_content["client_x509_cert_url"],
}

GcpCredentials(service_account_info=service_account_info).save("gcp-credential-block")
