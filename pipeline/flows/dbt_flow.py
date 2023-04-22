from prefect import flow
from prefect_dbt import DbtCoreOperation


@flow(retries=3)
def trigger_dbt_cli_command_flow():
    dbt_op = DbtCoreOperation.load("dbt-core-block")
    results = dbt_op.run()
