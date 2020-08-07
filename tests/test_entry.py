#!/usr/bin/env python

import pathlib
import pygame
from absolutris import entry
from absolutris import config_loader


def test_entry_provide_user_dir():
    assert entry.provide_user_dir(pathlib.Path(entry.dir_name)).is_dir()


cfg_path = entry.provide_user_dir(pathlib.Path(entry.dir_name)) / entry.ini_name
pygame.init()


def test_config_file_creation():
    with config_loader.Config(cfg_path) as config:
        assert config.path_to_config_file.exists()
        assert type(config.playfield_width) is int
        assert type(config.playfield_height) is int
        assert type(config.game_window_title) is str
        assert type(config.game_window_x_pos) is int
        assert type(config.game_window_y_pos) is int
        assert type(config.game_window_width) is int
        assert type(config.game_window_height) is int
        assert type(config.colors_window_bg) is pygame.Color
        assert type(config.colors_window_fg) is pygame.Color
        assert type(config.colors_window_font_color) is pygame.Color
        assert config.playfield_width > 0
        assert config.playfield_height > 0
        assert config.game_window_title
        assert config.game_window_x_pos >= 0
        assert config.game_window_y_pos >= 0
        assert config.game_window_width > 0
        assert config.game_window_height > 0


def test_config_file_deletion():
    assert not cfg_path.exists()

