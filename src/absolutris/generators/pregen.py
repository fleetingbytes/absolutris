#!/usr/bin/env python

import pathlib
import datetime
import requests
import shutil
from absolutris import config_loader
from absolutris import utils


def date_as_str(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d")


def file_url(date: datetime.datetime) -> str:
    return f"https://archive.random.org/download?file={date_as_str(date)}.bin"


def download_bytes(config: config_loader.Config) -> pathlib.Path:
    """
    downloads today's pregenerated file of random bits from archive.random.org
    and saves it in the specified directory
    and returns the pathlib.Path to it.
    """
    pregen_dir = utils.provide_dir(config.path_to_home / "pregen")
    date = datetime.datetime.today()
    target_file = pregen_dir / (date_as_str(date) + ".bin")
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
    url = file_url(date)
    response = requests.get(url, headers=headers)
    with open(target_file, mode="wb") as out_file:
        out_file.write(response.content)
    return target_file


if __name__ == "__main__":
    from absolutris import testhelper
    target_file = download_bytes(testhelper.config)

