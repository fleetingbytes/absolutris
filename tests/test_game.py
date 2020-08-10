#!/usr/bin/env python

import pytest
from absolutris import game
from absolutris import errors
from absolutris import testhelper


def test_raise_GuiNotImplemented() -> None:
    """
    Tests if GuiNotImplemented error is raised when user selected a not implemented or non-instantiated gui, e.g.
    $ absolutris -g missing_gui
    """
    with pytest.raises(errors.GuiNotImplemented):
        testhelper.config.cli = testhelper.Cli(gui="not_instantiated")
        game_test = game.Game(testhelper.config)


def test_game_gui_init() -> None:
    """
    Tests if a game session can be initialized with any gui
    """
    for gi_name, gi in testhelper.find_gui_instances():
        testhelper.config.cli = testhelper.Cli(gui=gi_name)
        assert game.Game(testhelper.config)


def test_no_gui_game() -> None:
    """
    Tests if a game session can be instantiated without gui
    """
    testhelper.config.cli = testhelper.Cli(gui=None)
    assert game.run(testhelper.config) is None
