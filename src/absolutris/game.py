#!/usr/bin/env python

import pygame
import os
import logging
# Necessary for Typing
from absolutris import config_loader
# Own modules
from absolutris import errors


# setup logging
logger = logging.getLogger(__name__)


class Game:
    """
    Main Game class.
    """
    def __init__(self, config: config_loader.Config) -> None:
        self.config = config
    def setup_game_window(self) -> None:
        # Set initial game window position
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.config.game_window_x_pos},{self.config.game_window_y_pos}"
        pygame.display.set_caption(self.config.game_window_title)
        self.game_window = pygame.display.set_mode(
                size=(self.config.game_window_width, self.config.game_window_height), 
                # flags=pygame.NOFRAME
            )
        self.game_window.fill(self.config.colors_window_bg)
    def run_game(self) -> None:
        logger.debug("Running game")
        pygame.init()
        self.setup_game_window()
        self.pygame_running = True
        logger.info(f"Running main game loop")
        while self.pygame_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pygame_running = False
                    break
                if event.type == pygame.KEYDOWN:
                    # Close main window if Ctrl-Q is pressed
                    if event.key == pygame.K_q:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_CTRL:
                            self.pygame_running = False
                            break
        logger.info(f"Finished main game loop")
        pygame.quit()
        logger.debug("Finished running game")


def run(config: config_loader.Config) -> None:
    logger.debug(f"Running GUI")
    game = Game(config)
    game.run_game()
    logger.debug(f"Ending GUI")


if __name__ == "__main__":
    logger.debug(f"GUI started")
    logger.debug(f"GUI ended")
