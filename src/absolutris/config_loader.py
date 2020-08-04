#!/usr/bin/env python

import pathlib
import configparser
import logging

# setup logging
logger = logging.getLogger(__name__)


class Config():
    """
    Holds all confituration data readily available as attributes
    """
    def __init__(self, cfg_path: pathlib.Path) -> None:
        self.path_to_config_file = cfg_path
        self.read_config_file()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        # Deleting config during development. Comment after release.
        self.delete_config_file()
        pass
    def read_config_file(self) -> None:
        """
        Reads current configuration file or creates a new one with a default configuration
        """
        self.config_parser = configparser.ConfigParser(allow_no_value=True)
        self.config_parser.optionxform = str
        try:
            self.config_parser.read_file(open(self.path_to_config_file))
            logger.info(f"{self.path_to_config_file} read")
            self.parse()
        except FileNotFoundError:
            logger.info("config file missing")
            self.create_config_file()
    def create_config_file(self) -> None:
        """
        Creates the default config file
        """
        logger.info(f"creating {self.path_to_config_file}")
        self.config_parser.add_section("Playfield")
        self.config_parser.set("Playfield", "# Playfield settings.")
        self.config_parser.set("Playfield", "width", "10")
        self.config_parser.set("Playfield", "height", "20")
        self.config_parser.add_section("Game window")
        self.config_parser.set("Game window", "# Pygame game window settings.")
        self.config_parser.set("Game window", "title", "Absolutris")
        self.config_parser.set("Game window", "# Initial game window position")
        self.config_parser.set("Game window", "initial_x_pos", "100")
        self.config_parser.set("Game window", "initial_y_pos", "100")
        self.config_parser.set("Game window", "# Game window dimensions")
        self.config_parser.set("Game window", "width", "800")
        self.config_parser.set("Game window", "height", "600")
        with open(self.path_to_config_file, mode="w", encoding="utf-8") as configfh:
            self.config_parser.write(configfh)
        self.read_config_file()
    def delete_config_file(self) -> None:
        """
        Serves debugging purposes. Deletes the config file.
        """
        try:
            self.path_to_config_file.unlink()
            logger.debug(f"{self.path_to_config_file} deleted")
        except FileNotFoundError as exc:
            logger.exception(f"Could not delete {self.path_to_config_file}")
    def parse(self) -> None:
        """
        Parses the configuration files into usable attributes
        """
        self.playfield_width = self.config_parser.getint("Playfield", "width")
        self.playfield_height = self.config_parser.getint("Playfield", "height")
        self.game_window_title = self.config_parser.get("Game window", "title")
        self.game_window_x_pos = self.config_parser.getint("Game window", "initial_x_pos")
        self.game_window_y_pos = self.config_parser.getint("Game window", "initial_y_pos")
        self.game_window_width = self.config_parser.getint("Game window", "width")
        self.game_window_height = self.config_parser.getint("Game window", "height")


if __name__ == "__main__":
    pass
