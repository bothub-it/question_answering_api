import os
import sys
import logging
import plac
import requests
import posixpath
from google.cloud import storage
from . import settings

logger = logging.getLogger(__name__)

# model_download_url = {
#     'pt_br': 'link',
#     'en': 'link',
#     'multilang': 'link'
# }

# def download_file(url, file_name):
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(file_name, "wb") as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)
#     return file_name


def find_occurrences(s, ch):  # to find position of '/' in blob path ,used to create folders in local storage
    return [i for i, letter in enumerate(s) if letter == ch]


def download_folder_structure_from_bucket(bucket, local_path, bucket_path):

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    blobs = list(bucket.list_blobs(prefix=bucket_path))
    print(blobs)
    for blob in blobs:
        start_loc = 0
        folder_loc = find_occurrences(blob.name.replace(bucket_path, ''), '/')
        if not blob.name.endswith("/"):
            if blob.name.replace(bucket_path, '').find("/") == -1:
                download_path = local_path + '/' + blob.name.replace(bucket_path, '')
                blob.download_to_filename(download_path)
            else:
                for folder in folder_loc:
                    if not os.path.exists(local_path + '/' + blob.name.replace(bucket_path, '')[start_loc:folder]):
                        create_folder = local_path + '/' + blob.name.replace(bucket_path, '')[0:start_loc] + '/' + blob.name.replace(bucket_path, '')[start_loc:folder]
                        start_loc = folder + 1
                        os.makedirs(create_folder)

                download_path = local_path + '/' + blob.name.replace(bucket_path, '')
                print(download_path)
                blob.download_to_filename(download_path)
                print(blob.name.replace(bucket_path, '')[0:blob.name.replace(bucket_path, '').find("/")])

    print('blob {} downloaded to {}.'.format(bucket_path, local_path))


def download_model(model):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('bothub_question_answering')

    model_dir = model
    os.makedirs(model_dir, exist_ok=True)

    # model_url = model_download_url.get(model)
    # download_file(model_url, posixpath.join(model_dir, model_file_name))

    logger.info("downloading bert")
    download_folder_structure_from_bucket(bucket, model_dir, model_dir)
    logger.info("finished downloading bert")


if __name__ == "__main__":
    if sys.argv[1:]:
        plac.call(download_model, sys.argv[1:])
    elif settings.model:
        plac.call(download_model, settings.model)
    else:
        print('no language selected, use --lang or set env var MODEL to your desired language')
