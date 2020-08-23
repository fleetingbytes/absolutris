#!/usr/bin/env python

import pathlib
from absolutris import utils


def test_utils_provide_dir():
    testdir = pathlib.Path.home() / "testdir"
    assert utils.provide_dir().is_dir()
    # shutil.rmtree(testdir) does not seem to be necessary, pytest is probably cleaning up all created dirs.


def test_utils_constants():
    assert utils.dir_name
    assert utils.ini_name
