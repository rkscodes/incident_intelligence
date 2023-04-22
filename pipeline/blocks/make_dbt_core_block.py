from prefect_dbt import DbtCoreOperation
from prefect_dbt.cli import DbtCliProfile

dbt_cli_profile = DbtCliProfile.load("dbt-cli-profile-block")


core = DbtCoreOperation(
    commands=["dbt clean", "dbt debug", "dbt seed --full-refresh", "dbt run"],
    stream_output=True,
    profiles_dir=".",
    project_dir="transform_dbt",
    overwrite_profiles=True,
    dbt_cli_profile=dbt_cli_profile,
)

core.save("dbt-core-block")
