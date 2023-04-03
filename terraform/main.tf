
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


resource "google_compute_instance" "deincidentcompute" {
  name         = "deincidentcompute"
  machine_type = "e2-custom-4-9216"
  zone         = var.zone
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-focal-v20230302"
      size  = "80"
      type  = "pd-balanced"
    }
  }

  network_interface {
    network = "default"
    # subnetwork = "regions/us-west1/subnetworks/default"
    subnetwork = "regions/${var.region}/subnetworks/default"
    access_config {
      #   name         = "External NAT"
      network_tier = "PREMIUM"
    }
  }

  allow_stopping_for_update = true

  metadata = {
    ssh-keys = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
  }

  tags = ["http-server", "https-server"]

  service_account {
    email = "557177865159-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring.write",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/service.management.readonly",
    "https://www.googleapis.com/auth/trace.append"]
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    provisioning_model  = "STANDARD"
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  deletion_protection = false
  description         = ""
  labels = {
    "ec-src" = "vm_add-rest"
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

resource "google_bigquery_dataset" "data-warehouse" {
  dataset_id                 = var.BQ_DATASET
  friendly_name              = "Police Incident Bigquery"
  description                = "This is warehouse to push data into from gcs for SF Police incident"
  location                   = var.region
  delete_contents_on_destroy = true
}
