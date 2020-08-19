#!/usr/bin/env python

import datetime
from absolutris.generators import pregen
from absolutris import testhelper


def test_download_bytes() -> None:
    d = pregen.download_bytes(testhelper.config)
    assert d.exists()

