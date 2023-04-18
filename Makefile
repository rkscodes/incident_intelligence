run: pipeline/flows/parent_etl_flow.py
	python pipeline/flows/parent_etl_flow.py

setup: install_poetry install_deps

install_poetry:
	pip install poetry

install_deps:
	poetry install --no-root --without dev

prefect_setup: prefect_gcp_install register_blocks

prefect_gcp_install:
	prefect block register -m prefect_gcp

register_blocks: pipeline/blocks/make_gcp_credentials.py pipeline/blocks/make_gcs_bucket.py
	python pipeline/blocks/make_json_block.py
	python pipeline/blocks/make_gcp_credentials.py
	python pipeline/blocks/make_gcs_bucket.py
	python pipeline/blocks/make_github_repo_block.py
	python pipeline/blocks/make_docker_container.py

deployment: 
	python pipeline/flows/infra-local-storage-github_deployment.py
	python pipeline/flows/infra-docker-storage-github_deployment.py

format:
	isort --profile black -l 100 ./
	black -l 100 ./

clean:
	rm -rf data/ data-gcs/ offset_dir/