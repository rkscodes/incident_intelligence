from prefect import task
from pipeline.utils.renamed_file_name import renamed_file_name


@task(log_prints=True)
def common_files_names(local_file_list, gcb_file_list):
    new_file_processed = []
    for file_name in local_file_list:
        temp = renamed_file_name(file_name)
        new_file_processed.append(temp)
    common_files = list(set(new_file_processed) & set(gcb_file_list))
    return common_files
