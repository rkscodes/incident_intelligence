locals {
  data_lake_bucket = "incident_data_lake"
}


variable "gce_ssh_user" {
  description = "SSH username"
  type        = string
  default     = "ram"
}

variable "gce_ssh_pub_key_file" {
  description = "SSH Public key location"
  type        = string
  default     = "/Users/ram/.ssh/gcp_deincident.pub"
}

variable "project" {
  default     = "affable-tangent-382517"
  type        = string
  description = "Project ID on gcp"
}

variable "region" {
  default     = "us-west1"
  type        = string
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
}


variable "zone" {
  default     = "us-west1-b"
  type        = string
  description = "Zone in which to setup the gcp"
}

variable "storage_class" {
  default     = "STANDARD"
  type        = string
  description = "Storage class type for your bucket. Check official docs for more info."

}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "police_incidents_warehouse"
}
