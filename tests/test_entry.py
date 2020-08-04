import pathlib
from absolutris import entry
from absolutris import config_loader


def test_entry_provide_user_dir():
    assert entry.provide_user_dir(pathlib.Path(entry.dir_name)).is_dir()


cfg_path = entry.provide_user_dir(pathlib.Path(entry.dir_name)) / entry.ini_name


def test_config_file_creation():
    with config_loader.Config(cfg_path) as config:
        assert config.path_to_config_file.exists()
        assert type(config.playfield_width) is int

def test_config_file_deletion():
    assert not cfg_path.exists()

