from parent_etl_flow import parent_etl_flow
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect.infrastructure import DockerContainer

github_block = GitHub.load("project-code")


docker_container_block = DockerContainer.load("docker-block")

deployment = Deployment.build_from_flow(
    flow=parent_etl_flow,
    name="infra-local-storage-local",
    # path="/",
    # entrypoint="pipeline/flows/parent_etl_flow.py:parent_etl_flow",
    ignore_file=".prefectignore",
    skip_upload=True,
)
deployment.apply()
