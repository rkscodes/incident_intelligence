from prefect.filesystems import GitHub
from prefect.blocks.system import JSON

json_block = JSON.load("json-config")
block = GitHub(
    repository=json_block.value["github_repo"], reference=json_block.value["branch"]
)
block.save("project-code")
