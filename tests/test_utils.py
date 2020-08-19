#!/usr/bin/env python

import pathlib
import shutil
from absolutris import utils

def test_utils_provide_dir():
    testdir = pathlib.Path.home() / "testdir"
    assert utils.provide_dir(testdir).is_dir()
    shutil.rmtree(testdir)

