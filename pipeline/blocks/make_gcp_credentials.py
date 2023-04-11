from prefect_gcp import GcpCredentials
from pathlib import Path

# replace this PLACEHOLDER dict with your own service account info
service_account_file = (
    Path.home() / ".config" / "affable-tangent-382517-239724fdc96c_terraform.json"
)

GcpCredentials(service_account_file=service_account_file).save("gcp-credential-block")
