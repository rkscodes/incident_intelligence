@flow(log_prints=True)
def update_gcb_file_if_already_exists(local_file_list: List, gcb_file_list: List):
    common_files = common_files_names(local_file_list, gcb_file_list)
    download_common_files_gcb(common_files)
    
    #joining the data 
    for files in common_files: 
        new_df = pd.read_csv(f'../../{files}')
        gcs_df = pd.read_csv(f'temp/{files}')
        df = pd.concat([gcs_df, new_df], axis= 0)
        df.to_csv(f'../../{files}'  , index=False)

    remove_downloaded_files_gcb('temp')


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
    if Path(dir).is_dir():
        shutil.rmtree(dir) 

