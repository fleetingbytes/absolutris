#!/usr/bin/env python

import pathlib
import datetime
import requests
import numpy
import io
from contextlib import contextmanager
from absolutris import config_loader
from absolutris import utils


def date_as_str(date: datetime.datetime) -> str:
    """
    Returns today's date in YYYY-MM-DD format
    """
    return date.strftime("%Y-%m-%d")


def file_url(date: datetime.datetime) -> str:
    """
    Returns the URL of today's random bytes archive
    """
    return f"https://archive.random.org/download?file={date_as_str(date)}.bin"


def download_bytes(config: config_loader.Config) -> pathlib.Path:
    """
    Downloads today's pregenerated file of random bits from archive.random.org
    and saves it in the pregen directory
    and returns the pathlib.Path to it.
    """
    pregen_dir = utils.provide_dir(config.path_to_home / "pregen")
    date = datetime.datetime.today()
    target_file = pregen_dir / (date_as_str(date) + ".bin")
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
    url = file_url(date)
    if not target_file.exists():
        response = requests.get(url, headers=headers)
        with open(target_file, mode="wb") as out_file:
            out_file.write(response.content)
    return target_file


@contextmanager
def init_file(file_path: pathlib.Path, offset: int) -> io.BufferedReader:
    file = open(file_path, mode="rb")
    _ = file.read(offset)
    try:
        yield file
    finally:
        file.close()


def int_from_file(file_handle, n_bytes: int) -> int:
    """
    Reads bytes from file and converts them to an int
    """
    b = file_handle.read(n_bytes)
    return int.from_bytes(b, byteorder="little", signed=False)


def list_from_int(i: int) -> list:
    s = numpy.base_repr(i, base=7)
    return s

if __name__ == "__main__":
    from absolutris import testhelper
    target_file = download_bytes(testhelper.config)
    offset = 0
    with init_file(target_file, offset) as file:
        while True:
            n_bytes = int(input("How many bytes to read?: "))
            i = int_from_file(file, n_bytes)
            s = list_from_int(i)
            try:
                ratio = len(s) / n_bytes
            except ZeroDivisionError:
                ratio = 0
            print(f"{int.bit_length(i) = }")
            print(f"{len(s) = }")
            print(f"{s[:1000] = }")
            print(f"{ratio = }")

