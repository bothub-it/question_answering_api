import logging
import plac
import os
import requests
import sys
import zipfile

logger = logging.getLogger(__name__)


def download_file(url, file_name):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_name


def download_models(model_urls):
    model_url = model_urls.split("|")
    for url in model_url:
        file_name = 'zipped_model.zip'
        logger.info("downloading qa model . . .")
        download_file(url, file_name)
        logger.info("extracting qa model . . .")
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove(file_name)


if __name__ == "__main__":
    """
    Downloads and extract one or more zipped models
    argv : link1|link2|...
    """
    plac.call(download_models, sys.argv[1:])
