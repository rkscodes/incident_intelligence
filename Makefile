run:
	python pipeline/flows/parent_etl_flow.py

env_setup: install_poetry install_dependencies

install_poetry:
	pip install poetry

install_dependencies:
	poetry install --no-root --without dev

prefect_setup: prefect_register_blocks create_blocks deployment profile_setup

prefect_register_blocks:
	-prefect block register -m prefect_gcp
	-prefect block register -m prefect_dbt

create_blocks:
	-python pipeline/blocks/make_json_block.py
	-python pipeline/blocks/make_gcp_credentials.py
	-python pipeline/blocks/make_gcs_bucket.py
	-python pipeline/blocks/make_github_repo_block.py
	-python pipeline/blocks/make_docker_container.py
	-python pipeline/blocks/make_dbt_cli_bigquery_target_block.py
	-python pipeline/blocks/make_dbt_cli_profile_block.py
	-python pipeline/blocks/make_dbt_core_block.py

remove_blocks:
	-prefect block delete json/json-config
	-prefect block delete docker-container/docker-block
	-prefect block delete gcp-credentials/gcp-credential-block
	-prefect block delete gcs-bucket/gcp-bucket-block
	-prefect block delete github/project-code
	-prefect block delete dbt-cli-bigquery-target-configs/dbt-cli-bigquery-target-block
	-prefect block delete dbt-cli-profile/dbt-cli-profile-block
	-prefect block delete dbt-core-operation/dbt-core-block

deployment: 
	-python pipeline/flows/infra-local-storage-github_deployment.py
	-python pipeline/flows/infra-docker-storage-github_deployment.py
	-python pipeline/flows/infra-docker-storage-docker_deployment.py
	-python pipeline/flows/infra-local-storage-local_deployment.py

profile_setup:
	prefect profile use default
	prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
	-prefect profile create remote

profile_remove: 
	-prefect profile use default
	-prefect profile delete remote
	-prefect config unset PREFECT_API_URL

format:
	isort --profile black -l 100 ./
	black -l 100 ./
	sqlfmt .

clean: remove_blocks profile_remove
	-rm -rf data/ data-gcs/ offset_dir/