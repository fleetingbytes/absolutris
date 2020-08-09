#!/usr/bin/env python

import pathlib
import configparser
import logging
import pygame

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
        self.config_parser.add_section("GUI")
        self.config_parser.set("GUI", "# GUI settings are not necessary here")
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
    def get_color(self, section: str, values: str) -> pygame.Color:
        """
        This converts color values from the config file to pygame.Color.
        """
        return pygame.Color(*(int(rgba_value) for rgba_value in self.config_parser.get(section, values).split(", ")))
    def parse(self) -> None:
        """
        Parses the configuration files into usable attributes
        """
        pass


if __name__ == "__main__":
    pass
