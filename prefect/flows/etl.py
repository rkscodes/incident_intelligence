from pathlib import Path
import pandas as pd 
from sodapy import Socrata
from datetime import datetime, timedelta
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from typing import List
import shutil


client = Socrata("data.sfgov.org", None)


@task()
def fetch_data_api(offset: int):
    records_count = client.get("wg3w-h783", select="count(*)")
    total_no_of_records = int(records_count[0]['count'])

    api_data = pd.DataFrame()

    while total_no_of_records != offset: 
        results = client.get("wg3w-h783", offset=offset, limit=50000)
        results_df = pd.DataFrame.from_records(results)
        api_data = pd.concat([api_data, results_df])
        
        offset += len(results_df)
        offset

    with open("offset.txt", "w+") as f: 
        f.write(str(offset))

    return api_data


def dump_data_info_test(api_data):
    if api_data is None: 
        return 
    print(api_data.dtypes)
    print(api_data.head())


@task()
def augment_data(api_data):
    # Extract month and date from the incident_date column s

    col = pd.DatetimeIndex(api_data['incident_date']).month.astype(str).str.zfill(2)
    api_data.insert(loc=4,column='incident_month',value=col )

    col = pd.DatetimeIndex(api_data['incident_date']).day.astype(str).str.zfill(2)
    api_data.insert(loc=5, column="incident_day", value=col)

    api_data['incident_year'] = api_data['incident_year'].astype(str)
    
    return api_data


@task()
def save_data_locally(api_data_augmented):
    # Create directory structure if it doesn't exist
    for year in api_data_augmented['incident_year'].unique():
        year_dir = Path('../../data') / year 
        year_dir.mkdir(parents=True, exist_ok=True)
        for month in api_data_augmented[api_data_augmented['incident_year'] == year]['incident_month'].unique():
            month_dir = year_dir / month
            month_dir.mkdir(parents=True, exist_ok=True)

    # Save the DataFrame into year/month/day CSV files
    for _, row in api_data_augmented.iterrows():
        file_path = Path('../../data') / row['incident_year'] / row['incident_month'] / f"{row['incident_day']}.csv"
        row.to_frame().T.to_csv(file_path, mode='a', header=not file_path.exists(), index=False)

@task()   
def check_recently_modified_files():
    # Check for recently modified files

    # Specify the directory to search for files in
    directory_path = Path('../../data/')

    # Calculate the datetime range for today
    today = datetime.today()
    start_time = datetime(today.year, today.month, today.day)
    end_time = start_time + timedelta(days=1)

    # Loop through all files in the directory and get the paths of the ones modified today
    local_file_list = []
    for file_path in directory_path.glob('**/*'):
            if file_path.is_file():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if start_time <= mtime < end_time and "ipynb_checkpoints" not in str(file_path):
                    local_file_list.append(str(file_path))

    return local_file_list

@task
def check_existing_data_in_gcb():
    gcs_block =  GcsBucket.load("gcp-bucket-block")

    #Load all blobs from gcs 
    blob_list = gcs_block.list_blobs()
    gcb_file_list = [blob.name for blob in blob_list]
    return gcb_file_list



def renamed_local_file(path: str):
    # file_name = str(path)
    parts = path.split('/')
    just_name = parts[-1].split('.')[-2]
    new_name = parts[-4]+ '/'+parts[-3] + '/' + parts[-2] + '/' + just_name + '.csv'
    return new_name


@task
def common_files_names(local_file_list, gcb_file_list):
    new_file_processed = []
    for file_name in local_file_list:
        temp = renamed_local_file(file_name)
        new_file_processed.append(temp)
    common_files = list(set(new_file_processed) & set(gcb_file_list))
    return common_files


@task
def download_common_files_gcb(common_files: List):
    for files in common_files:
        to_path_dir = Path('temp') / Path(files).parent
        to_path_dir.mkdir( parents = True, exist_ok= True)
        # to_path_name = Path(to_path_dir + '/' + str(Path(files).name))
        to_path_name = to_path_dir / Path(files).name

        print("Downloading to path", to_path_name)

        gcs_block =  GcsBucket.load("gcp-bucket-block")
        gcs_block.download_object_to_path(from_path=files , to_path=to_path_name)


@task
def remove_downloaded_files_gcb(dir: str):
    shutil.rmtree(dir)



@flow
def update_gcb_file_if_already_exists(local_file_list: List, gcb_file_list: List):
    common_files = common_files_names(local_file_list, gcb_file_list)
    download_common_files_gcb(common_files)
    
    #joining the data 
    for files in common_files: 
        new_df = pd.read_csv(f'../../{files}')
        gcs_df = pd.read_csv(f'temp/{files}')
        df = pd.concat([gcs_df, new_df], axis= 0 , index=False)
        df.to_csv(f'../../{files}')

    remove_downloaded_files_gcb('temp')


@flow(log_prints=True)                
def extract(offset: int):
    # api_data = fetch_data_api(offset)
    # api_data_augmented = augment_data(api_data)
    # dump_data_info_test(api_data_augmented) 
    # save_data_locally(api_data_augmented)
    local_file_list = check_recently_modified_files()
    gcb_file_list = check_existing_data_in_gcb()
    update_gcb_file_if_already_exists(local_file_list, gcb_file_list)
    # fetch_existing_data_gcb()
    # remove_data_local() in 




@flow(log_prints=True)
def etl_flow(offset: int = 0):
    extract(offset)


if __name__ == "__main__":
    # get offset 
    offset = '0'
    try:
        with open("offset.txt", "r") as f:
            offset = f.readline()
    except FileNotFoundError:
        with open("offset.txt", "w+") as f:
            f.write("0")     
    offset = int(offset)
     
    etl_flow(offset=714500)

# idea store offset value in .yaml file 
# also store base of the project in that file
# make download path with respect to variable in this project 