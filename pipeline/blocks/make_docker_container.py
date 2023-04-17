from prefect.blocks.system import JSON
from prefect.infrastructure import DockerContainer

json_block = JSON.load("json-config")

docker = DockerContainer(
    image=json_block.value["docker_image"],
    image_pull_policy="IF_NOT_PRESENT",
    auto_remove=True,
)
docker.save("docker-block")
