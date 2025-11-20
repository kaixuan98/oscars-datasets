import os
import boto3

s3 = boto3.client('s3')
BASE_LOCAL_RAW_DATA = "../data/raw"
target_bucket = "oscars-ducklake"


def upload_to_s3(file_paths: list[str]):
    # find the file 
    for f in file_paths:
        object_name = os.path.basename(f)
        local_file = os.path.join(BASE_LOCAL_RAW_DATA, f)
        s3.upload_file(local_file, target_bucket, object_name)
    return True

