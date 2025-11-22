from kaggle.api.kaggle_api_extended import KaggleApi
import os

BASE_LOCAL_RAW_DATA = "data/raw"


def download_kaggle_dataset(sources: list[str]):
    api = KaggleApi()
    api.authenticate()

    all_files_name = []

    for s in sources:
        api.dataset_download_files(s, path=BASE_LOCAL_RAW_DATA, unzip=True)
        files = api.dataset_list_files(s).files
        all_files_name.extend([f.name for f in files])

    return all_files_name
