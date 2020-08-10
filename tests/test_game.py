#!/usr/bin/env python

import pytest
from absolutris import config_loader
from absolutris import entry
from absolutris import game
from absolutris import errors


config_dir = entry.provide_user_dir(entry.dir_name)


def test_raise_GuiNotImplemented() -> None:
    """
    Tests if GuiNotImplemented error is raised when user selected a not implemented or non-instantiated gui, e.g.
    $ absolutris -g missing_gui
    """
    with pytest.raises(errors.GuiNotImplemented):
        with config_loader.Config(config_dir / entry.ini_name) as config:
            pass
        class Cli:
            gui = "not_instantiated"
        config.cli = Cli()
        game_test = game.Game(config)
