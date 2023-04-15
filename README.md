# Incidence Intelligence 🔍

A data pipeline that utilizes the ELT (Extract, Load, Transform) process to fetch, load, and transform San Francisco Police Department incident data, with the aim of generating insights.

## Tech Stack

**Infrastructure**: Terraform

**Cloud:** Google Cloud

**Data lake:** Google Cloud Storage

**Data warehouse:** BigQuery

**Orchestration:** Prefect

**Data transformation:** DBT

**Data visualization:** Google Looker Studio




## Demo

Insert gif or link to demo


## Screenshots

<!-- ![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here) -->

## Installation

### Install Project
1. Refer  [Setup Terraform](#setup-terraform) 
2. Git clone project on GCP: ``
3. Change to cloned directory: `git clone https://github.com/rkscodes/incident_intelligence.git`
4. Refer [Setup GCP Cloud](#setup-gcp-cloud) 
5. Activate the conda-env: `conda activate <env-name> `
6. Setup `config.json` with required details, change `offset` to 0 to fetch from start
7. Setup `/terrafrom/variables.tf` with your cloud details 
8. Install all required dependency: `make setup`
9. Start prefect server: `prefect server start`
10. Register `prefect-gcp` and `blocks` using: `make prefect_setup`
11. Run the ETL : `make run`

### Setup Terraform
1. [Install terraform on your pc](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli)
2. Clone this or forked repo on remote machine `git clone https://github.com/rkscodes/incident_intelligence.git`
3. `cd incident_intelligence/terraform`
4. Refer [Setup GCP](#setup-gcp) and follow all steps.
5. Update `project`  var in `variables.tf` with GCP project id.
6. Authenticate the service first:
   - `export GOOGLE_APPLICATION_CREDENTIALS={{path_to_application_credential}}`
   - `gcloud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS}`
7. Generate a SSH key using: `ssh-keygen -t rsa -f ~/.ssh/<name> -C <username> -b 2048`
8. Update `gce_ssh_user, gce_ssh_pub_key_file` variable in `variables.tf` with generated public key username and location. 
9. Optionally could modify `region, zone, data_lake_bucket` if required
10. Please make sure you have exported `export GOOGLE_APPLICATION_CREDENTIALS={{path_to_application_credential}}`  before running below commands in same shell 
11. `terraform validate`
12. `terraform plan`
13. `terraform apply`
14. Your infra should be up and running. 
15. One caveat if you decide to use `terraform destroy` VPC network are sometimes not destroyed so destroy `my-network` manually in case. 

### Setup GCP
1. [Terraform reference for GCP](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#set-up-gcp)
2. [Create GCP Account](https://console.cloud.google.com/freetrial/)
3. [Setup a GCP Project](https://console.cloud.google.com/projectcreate)
4. [Enable google compute api](https://console.developers.google.com/apis/library/compute.googleapis.com)
5. [Create a service account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey)

### Setup GCP Cloud
1. Connect to `gcp-instance` : `ssh -i <input_ssh_file> user@ip`
2. Download Minconda on gcp: `wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh`
3. `chmod +x ./Miniconda3-py39_23.1.0-1-Linux-x86_64.sh`
4. `./Miniconda3-py39_23.1.0-1-Linux-x86_64.sh`
5. create conda env : `conda create --name <name> python=3.9`
6. activate it: `conda activate <env-name>`
7. Install poetry: `pip install poetry`

## Roadmap

- placeholder


## Appendix

Any additional information goes here


## Acknowledgements

 - placeholder


## License

[Apache License](LICENSE)

