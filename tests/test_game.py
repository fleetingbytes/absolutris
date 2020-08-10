#!/usr/bin/env python

import pytest
import pygame
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


def test_game_with_gui() -> None:
    """
    Tests the instance fuinctions of game.Game()
    """
    # test for every gui instance:
    for gi_name, gi in testhelper.find_gui_instances():
        testhelper.config.cli = testhelper.Cli(gui=gi_name)
        # test Game.__init__()
        game_instance = game.Game(testhelper.config)
        assert type(game_instance) is game.Game
        # test Game.setup_game_window()
        pygame.init()
        game_instance.setup_game_window()
        assert type(game_instance.game_window) is pygame.Surface
        # run gui with a testing hook
        # wrap = testhelper.pygame_wrapper(game_instance.run_gui(testing=True))
        game_instance.run_gui()
        # wrap.send(None)
        # create some event
        # TEST_EVENT = game.pygame.event.custom_type()
        # assert TEST_EVENT
        # inject event
        # test_event = pygame.event.Event(TEST_EVENT)
        # wrap.send(test_event)


def test_no_gui_game() -> None:
    """
    Tests if a game can be run without gui
    """
    testhelper.config.cli = testhelper.Cli(gui=None)
    assert game.run(testhelper.config) is None
