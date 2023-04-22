from prefect.blocks.system import JSON
from prefect_dbt.cli import DbtCliProfile
from prefect_dbt.cli.configs import BigQueryTargetConfigs

bigquery_target_configs = BigQueryTargetConfigs.load("dbt-cli-bigquery-target-block")
json_block = JSON.load("json-config")

dbt_cli_profile = DbtCliProfile(
    name="transform_dbt",
    target="dev",
    target_configs=bigquery_target_configs,
)

dbt_cli_profile.save("dbt-cli-profile-block")
