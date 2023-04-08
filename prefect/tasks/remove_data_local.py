@task
def remove_data_local():
    if Path('../../data/').is_dir():
        shutil.rmtree('../../data/')