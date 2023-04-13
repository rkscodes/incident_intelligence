from pathlib import Path


def renamed_file_name(path: Path):
    file_name = str(path)
    parts = file_name.split("/")
    just_name = parts[-1].split(".")[-2]
    new_name = parts[-4] + "/" + parts[-3] + "/" + parts[-2] + "/" + just_name + ".csv"
    return Path(new_name)
