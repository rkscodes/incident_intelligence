from prefect.blocks.system import JSON
from prefect.filesystems import GitHub

json_block = JSON.load("json-config")
block = GitHub(
    repository=json_block.value["github_repo"],
    reference=json_block.value["branch"],
    include_git_objects=False,
)
block.save("project-code")
