@task
def renamed_local_file(path: str):
    # file_name = str(path)
    parts = path.split('/')
    just_name = parts[-1].split('.')[-2]
    new_name = parts[-4]+ '/'+parts[-3] + '/' + parts[-2] + '/' + just_name + '.csv'
    return new_name