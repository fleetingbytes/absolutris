import pygame
import configparser
from pathlib import Path


pygame.init()
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str


def read_or_create_config_file(path_to_configfile):
    """
    Creates config file with default values
    or reads the current config file "config.ini".
    """
    if not path_to_configfile.is_file():
        config.add_section("Display")
        config.set("Display", "# Settings related to the program window")
        config.set("Display", "window_horizontal", "800")
        config.set("Display", "window_vertical", "600")
        with open(path_to_configfile, mode="w", encoding="utf-8") as configfh:
            config.write(configfh)
    config.read(path_to_configfile)
    return config


if __name__ == "__main__":
    configfilepath = Path("config.ini")
    config = read_or_create_config_file(configfilepath)
    print(config["Display"]["window_horizontal"])
