
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region

}

resource "google_compute_network" "network" {
  name = "my-network"
}

resource "google_compute_subnetwork" "subnetwork" {
  name          = "my-subnetwork"
  region        = var.region
  network       = google_compute_network.network.id
  ip_cidr_range = "10.0.0.0/24"
}


resource "google_compute_firewall" "allow443" {
  name        = "allow443"
  network     = "default"
  direction   = "INGRESS"
  priority    = 1000
  description = "I am allowing this port so that I can access ssh on port 443, because in NIT port 22 seems blocked."

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  allow {
    protocol = "udp"
    ports    = ["443"]
  }

  source_ranges = ["0.0.0.0/0"]
}


# resource "google_compute_instance" "deincidentcompute" {
#   name         = "deincidentcompute"
#   machine_type = "e2-custom-4-9216"
#   zone         = var.zone

#   boot_disk {
#     auto_delete = true
#     initialize_params {
#       image = "ubuntu-os-cloud/ubuntu-2004-focal-v20230302"
#       size  = "80"
#       type  = "pd-balanced"
#     }
#     mode = "READ_WRITE"
#   }

#   network_interface {
#     network = "default"
#     # subnetwork = "regions/us-west1/subnetworks/default"
#     # subnetwork = "regions/${var.region}/subnetworks/default"
#     subnetwork = "projects/${var.project}/regions/${var.region}/subnetworks/default"

#     access_config {
#       #   name         = "External NAT"
#       network_tier = "PREMIUM"
#     }
#   }

#   can_ip_forward      = false
#   deletion_protection = false
#   enable_display      = false

#   allow_stopping_for_update = true


#   tags = ["http-server", "https-server"]

#   scheduling {
#     automatic_restart   = true
#     on_host_maintenance = "MIGRATE"
#     provisioning_model  = "STANDARD"
#     preemptible         = false
#   }

#   shielded_instance_config {
#     enable_integrity_monitoring = true
#     enable_secure_boot          = false
#     enable_vtpm                 = true
#   }

#   labels = {
#     "ec-src" = "vm_add-rest"
#   }
#   metadata = {
#     ssh-keys = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
#   }
# }


resource "google_compute_instance" "ii-free-tier" {
  name         = "ii-free-tier"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    auto_delete = true
    device_name = "free-tier"

    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20230302"
      size  = 30
      type  = "pd-standard"
    }

    mode = "READ_WRITE"
  }

  network_interface {
    access_config {
      network_tier = "STANDARD"
    }
    subnetwork = "projects/${var.project}/regions/${var.region}/subnetworks/default"
  }

  can_ip_forward            = false
  deletion_protection       = false
  enable_display            = false
  allow_stopping_for_update = true

  labels = {
    ec-src = "vm_add-tf"
  }

  tags = ["http-server", "https-server"]




  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }


  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  metadata = {
    ssh-keys = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
  }

}


resource "google_storage_bucket" "data-lake-bucket" {
  location = var.region
  name     = "${local.data_lake_bucket}_${var.project}"

  #optional settings 
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
  public_access_prevention = "enforced"
  force_destroy            = true
}

resource "google_bigquery_dataset" "police_incidents" {
  dataset_id                 = var.BQ_DATASET
  friendly_name              = "Police Incident Bigquery"
  description                = "This is warehouse to push data into from gcs for SF Police incident"
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "staging" {
  dataset_id                 = "staging"
  friendly_name              = "DBT staging area"
  description                = "This database contains stage models used in dbt"
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "core" {
  dataset_id                 = "core"
  friendly_name              = "DBT core area"
  description                = "This database will contains final tables for stakeholders"
  location                   = var.region
  delete_contents_on_destroy = true
}
