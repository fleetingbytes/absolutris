from typing import NoReturn
import pathlib
import logging
import logging.config
import sys
import argparse

#Own modules
from absolutris import logging_conf
from absolutris import config_loader


dir_name = "absolutris"
ini_name = "absolutris.config"


def provide_user_dir(dir_name: pathlib.Path) -> pathlib.Path:
    """
    Checks if there is a directory of name `dir_name` in the user home path.
    If not, it will try to create one. 
    """
    directory = pathlib.Path.home() / dir_name
    if directory.exists() and directory.is_dir():
        pass
        # logger.debug(f"Found {str(directory)}")
    else:
        directory.mkdir()
        # logger.info(f"Created {str(directory)}")
    return directory


# Setup logging
try:
    path_to_dir = provide_user_dir(dir_name)
    logger_config = logging_conf.create_dict_config(path_to_dir, "debug.log", "errors.log")
except FileExistsError:
    logger.error(f"Failed to create the directory `{str(path_to_dir)}` because it already exists as a file.")
    logger.info(f"Please create the directory `{str(path_to_dir)}`")
finally:
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger("custom_logger")


# Parse CLI arguments
def parse_cli_arguments(config) -> NoReturn:
    """
    Parse command line arguments and add them to config object
    """
    parser = argparse.ArgumentParser(description="Absolutris: My kind of tetris")
    parser.add_argument("-t", "--text", action="store_true")
    parser.add_argument("-s", "--stats", action="store_true")
    config.parsed_args = parser.parse_args(sys.argv[1:])


def cli_start() -> NoReturn:
    """
    Start from command line
    """
    logger.debug("Program started")
    with config_loader.Config(path_to_dir / ini_name) as config:
        parse_cli_arguments(config)
        logger.debug(f" Parsed arguments: {config.parsed_args}")
    logger.debug("Program ended")


if __name__ == "__main__":
    cli_start()
