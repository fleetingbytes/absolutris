#!/usr/bin/env python

import pygame
import os
import logging
import collections
# Necessary for Typing
from absolutris import config_loader
# Own modules
from absolutris import errors
from absolutris import menu


# setup logging
logger = logging.getLogger(__name__)


class Game:
    """
    Main Game class.
    """
    def __init__(self, config: config_loader.Config) -> None:
        self.config = config
        # Load GUI
        if self.config.cli.gui in ("default", "cli", None):
            if self.config.cli.gui != "cli":
                logger.debug("using default gui")
            else:
                logger.debug("will use command line as gui")
            from absolutris.gui import default as gui
        elif self.config.cli.gui == "debug":
            logger.debug("using DEBUG gui")
            from absolutris.gui import debug as gui
        elif self.config.cli.gui == "m":
            logger.debug("using malicious gui")
            from absolutris.gui import m as gui
        else:
            raise errors.GuiNotImplemented(f"Cannot find any instance of \"{self.config.cli.gui}\" in gui.py")
        self.gui = gui
        # Load game plan
        if (self.config.cli.plan == "default") or (self.config.cli.plan is None):
            from absolutris.plans import default as plan
            logger.debug("using default plan")
            self.plan = plan
        else:
            raise errors.PlanNotImplemented(f"Cannot find any instance of \"{self.config.cli.plan}\" in plan.py")
    def setup_game_window(self) -> None:
        # Set initial game window position
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.gui.game_window_x_pos},{self.gui.game_window_y_pos}"
        pygame.display.set_caption(self.gui.game_window_title)
        self.game_window = pygame.display.set_mode(
                size=(self.gui.game_window_width, self.gui.game_window_height), 
                flags=self.gui.flags
            )
        self.game_window.fill(self.gui.colors_window_bg)
    def run_gui(self, testing: bool=False) -> None:
        """
        Tetris implementation with a pygame GUI.
        """
        logger.debug(f"Running game with {self.config.cli.gui} gui")
        pygame.init()
        self.setup_game_window()
        self.pygame_running = True
        logger.info(f"Entering main game loop")
        while self.pygame_running:
            # if testing:
                # test_input = (yield)
                # pygame.event.post(test_input)
            for event in pygame.event.get():
                # React to quitting pygame, e.g. by closing the game window
                if event.type == pygame.QUIT:
                    logger.debug("User closed pygame window")
                    self.pygame_running = False
                    break
                # React to keypresses:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # distinguish between Q and Ctrl-Q
                        mods = pygame.key.get_mods()
                        # End main loop if Ctrl-Q was pressed
                        if mods & pygame.KMOD_CTRL:
                            logger.debug("User pressed Ctrl-Q to quit the game")
                            self.pygame_running = False
                            break
        logger.info(f"Left main game loop")
        pygame.quit()
        logger.debug("Finished running game with {self.config.cli.gui} gui")
    def run_nogui(self) -> None:
        """
        Tetris implementation without pygame GUI.
        Used for testing and debugging purposes.

        We will still use the instance gui.debug, but will ignore only use
        the non-graphic-related attributes like playfield size etc.
        """
        logger.debug("Runing game with no gui")
        textmenu = menu.Text_Menu()
        options = collections.OrderedDict((
                ("Z", "Show next_pieces"),
                ("X", "Pull from next_pieces"),
                ("M", "Show Menu"),
                ("Q", "Quit"),
                ))
        textmenu.show(options)
        while True:
            key = textmenu.wait_key()
            if key not in options.keys():
                continue
            elif key == "Z":
                logger.info(f"{self.plan.next_window.window = }")
            elif key == "X":
                logger.info(f"Tetromino: {self.plan.next_window.window} --> {next(self.plan.next_window)} --> {self.plan.next_window.window}")
            elif key == "M":
                textmenu.show(options)
            elif key == "Q":
                break
        logger.debug("Finished runing game with no gui")


def run(config: config_loader.Config) -> None:
    if config.cli.download:
        logger.debug("Downloading random bits")
        pregen.download_bytes()
    else:
        game = Game(config)
        if config.cli.gui != "cli":
            game.run_gui()
        else:
            game.run_nogui()


if __name__ == "__main__":
    logger.debug(f"GUI started from __main__")
    logger.debug(f"GUI ended from __main__")
