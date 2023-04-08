from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket



from_path = Path('../../data/2023/03/06.csv').resolve()
to_path = Path('data/2023/03/06.csv')

gcs_block =  GcsBucket.load("gcp-bucket-block")
gcs_block.upload_from_path(from_path=from_path, to_path=to_path)

# gcs_block.download_folder_to_path(from_folder="data/2023/03/", to_folder="data")
# gcs_block.download_object_to_path(from_path='data/2023/03/27.csv' ,to_path= 'abc.csv')


# blob_list = gcs_block.list_blobs()

# file_paths = [blob.name for blob in blob_list]

# if str(to_path) in file_paths: 
#     print("true that")

# print(file_paths)