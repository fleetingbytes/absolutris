#!/usr/bin/env python

import datetime
import pytest
import random
import itertools
from absolutris.generators import pregen
from absolutris import testhelper
from absolutris import errors


def test_date_as_str() -> None:
    date = datetime.datetime.today()
    date_str = pregen.date_as_str(date)
    assert type(date_str) is str
    date_str_date = datetime.datetime.fromisoformat(date_str)
    assert date_str_date.year == date.year
    assert date_str_date.month == date.month
    assert date_str_date.day == date.day


def test_file_url() -> None:
    now = datetime.datetime.today()
    url = pregen.file_url(now)
    parts = url.split(pregen.date_as_str(now))
    assert "random.org" in parts[0]
    assert ".bin" in parts[-1]


def test_download_bytes() -> None:
    d = pregen.download_bytes()
    assert d.exists()


def test_rfh() -> None:
    # check if Random_File_Handler raises an error when wrongly instantiated:
    file_path = testhelper.create_random_bytes_file(bytes(tuple(random.randint(0, 255) for _ in range(1024*1024))))
    with pytest.raises(ValueError):
        pregen.Random_File_Handler(file_path, buffer_length=0)
    with pytest.raises(ValueError):
        pregen.Random_File_Handler(file_path, buffer_length=-1)
    assert isinstance(pregen.Random_File_Handler(file_path, buffer_length=1), pregen.Random_File_Handler)
    assert isinstance(pregen.Random_File_Handler(file_path, buffer_length=2), pregen.Random_File_Handler)
    assert isinstance(pregen.Random_File_Handler(file_path, buffer_length=50), pregen.Random_File_Handler)
    rfh = pregen.Random_File_Handler(file_path, buffer_length=100)
    assert isinstance(rfh, pregen.Random_File_Handler)
    assert file_path.with_suffix(".pos").exists()
    with open(file_path.with_suffix(".pos"), mode="wb") as pos_file:
        pos_file.write((pregen.RANDOM_FILE_BIT_LENGTH - 1000).to_bytes(length=pregen.MINO_BIT_LENGTH, byteorder="big", signed=False))
    # Test rfh.pop()
    with pytest.raises(errors.RandomSourceDepleted):
        while True:
            assert rfh.pop() is not None
    with open(file_path.with_suffix(".pos"), mode="rb") as pos_file:
        assert int.from_bytes(pos_file.read(), byteorder="big", signed=False) == pregen.RANDOM_FILE_BIT_LENGTH
    file_path.with_suffix(".pos").unlink()
    file_path.unlink()


