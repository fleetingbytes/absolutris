#!/usr/bin/env python

import pathlib
from absolutris import entry
from absolutris import utils
from absolutris import config_loader


cfg_path = utils.provide_dir(pathlib.Path(entry.dir_name)) / entry.ini_name


def test_config_file_creation():
    with config_loader.Config(cfg_path) as config:
        assert config.path_to_config_file.exists()


def test_config_file_deletion():
    assert not cfg_path.exists()

