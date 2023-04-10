from prefect import flow
from update_gcb_flow import update_gcb_file_if_already_exists
from tasks.fetch_data_api import fetch_data_api
from tasks.augment_data import augment_data
from tasks.save_data_locally import save_data_locally
from tasks.check_recently_modified_files import check_recently_modified_files
from tasks.check_existing_files_in_gcb import check_existing_files_in_gcb


@flow(log_prints=True)
def extract(offset: int):
    api_data = fetch_data_api(offset)
    api_data_augmented = augment_data(api_data)
    # dump_data_info_test(api_data_augmented)
    save_data_locally(api_data_augmented)
    local_file_list = check_recently_modified_files()
    gcb_file_list = check_existing_files_in_gcb()
    update_gcb_file_if_already_exists(local_file_list, gcb_file_list)
    return local_file_list
