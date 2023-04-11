import hashlib


def compute_hash(row):
    row_str = " ".join([str(val) for val in row.values])

    hash_value = hashlib.md5(row_str.encode()).hexdigest()
    return hash_value
