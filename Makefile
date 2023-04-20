run: pipeline/flows/parent_etl_flow.py
	python pipeline/flows/parent_etl_flow.py

setup: install_poetry install_deps

install_poetry:
	pip install poetry

install_deps:
	poetry install --no-root --without dev

prefect_setup: prefect_gcp_install register_blocks deployment

prefect_gcp_install:
	-prefect block register -m prefect_gcp

register_blocks: pipeline/blocks/make_gcp_credentials.py pipeline/blocks/make_gcs_bucket.py
	-python pipeline/blocks/make_json_block.py
	-python pipeline/blocks/make_gcp_credentials.py
	-python pipeline/blocks/make_gcs_bucket.py
	-python pipeline/blocks/make_github_repo_block.py
	-python pipeline/blocks/make_docker_container.py

remove_blocks:
	-prefect block delete json/json-config
	-prefect block delete docker-container/docker-block
	-prefect block delete gcp-credentials/gcp-credential-block
	-prefect block delete gcs-bucket/gcp-bucket-block
	-prefect block delete github/project-code

deployment: 
	-python pipeline/flows/infra-local-storage-github_deployment.py
	-python pipeline/flows/infra-docker-storage-github_deployment.py
	-python pipeline/flows/infra-docker-storage-local_deployment.py
	-python pipeline/flows/infra-local-storage-local_deployment.py


format:
	isort --profile black -l 100 ./
	black -l 100 ./
	sqlfmt .

clean: remove_blocks
	-rm -rf data/ data-gcs/ offset_dir/