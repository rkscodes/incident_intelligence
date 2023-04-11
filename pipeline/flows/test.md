    gcloud compute instances describe deincidentcompute --zone us-west1-b --project affable-tangent-382517 --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
