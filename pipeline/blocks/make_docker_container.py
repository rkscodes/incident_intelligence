from prefect.infrastructure import DockerContainer

docker = DockerContainer(
    image="rkscodes/incidence_intelligence:v001",
    image_pull_policy="IF_NOT_PRESENT",
    auto_remove=True,
)
docker.save("docker-block")
