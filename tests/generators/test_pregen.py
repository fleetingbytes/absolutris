#!/usr/bin/env python

import datetime
from absolutris.generators import pregen
from absolutris import testhelper


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
    d = pregen.download_bytes(testhelper.config)
    assert d.exists()

