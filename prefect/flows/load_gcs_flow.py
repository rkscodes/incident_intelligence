@flow(log_prints=True)
def load_gcs_flow(files: List ):
    gcs_block =  GcsBucket.load("gcp-bucket-block")

    for path in files: 
        from_path = path 
        to_path = renamed_local_file(path)
        gcs_block.upload_from_path(from_path=from_path, to_path=to_path)

