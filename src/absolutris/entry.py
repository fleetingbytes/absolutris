#!/usr/bin/env python

import pathlib
import logging
import logging.config
import sys
import argparse
import time

#Own modules
from absolutris import logging_conf
from absolutris import config_loader
# from absolutris import generators


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
def setup_logging_directory(dir_name):
    """
    Returns a logger.
    """
    try:
        path_to_dir = provide_user_dir(dir_name)
        logger_config = logging_conf.create_dict_config(path_to_dir, "debug.log", "errors.log")
    except FileExistsError:
        logger.error(f"Failed to create the directory `{str(path_to_dir)}` because it already exists as a file.")
        logger.info(f"Please create the directory `{str(path_to_dir)}`")
    finally:
        logging.config.dictConfig(logger_config)
        logger = logging.getLogger("custom_logger")
    return logger, path_to_dir


# Parse CLI arguments
def parse_cli_arguments() -> argparse.Namespace:
    """
    Parse command line arguments and add them to config object
    """
    parser = argparse.ArgumentParser(description="Absolutris: My kind of tetris")
    parser.add_argument("-g", "--gui", type=str, help="define which GUI to use")
    parser.add_argument("-s", "--stats", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args(sys.argv[1:])


def cli_start() -> None:
    """
    Start from command line
    """
    logger, path_to_dir = setup_logging_directory(dir_name)
    logger.debug("Program started")
    with config_loader.Config(path_to_dir / ini_name) as config:
        config.cli = parse_cli_arguments()
        logger.debug(f" Parsed arguments: {config.cli}")
    if config.cli.gui:
        from absolutris import game
        try:
            game.run(config)
        except Exception as err:
            logger.exception(f"Uncaught exception {repr(err)} occurred.")
    else:
        logger.debug("Running without GUI")
    logger.debug("Program ended")


if __name__ == "__main__":
    cli_start()
