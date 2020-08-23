#!/usr/bin/env python

import pathlib
import logging
import logging.config
import sys
import argparse
import time

#Own modules
from absolutris import utils
from absolutris import logging_conf
from absolutris import config_loader
from absolutris import game
# from absolutris import generators


# Setup logging
def setup_logging_directory():
    """
    Returns a logger.
    """
    try:
        path_to_dir = utils.provide_dir()
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
    parser.add_argument("-d", "--download", action="store_true", help="download random bytes from random.org")
    return parser.parse_args(sys.argv[1:])


def cli_start() -> None:
    """
    Start from command line
    """
    logger, path_to_dir = setup_logging_directory()
    logger.debug("Program started")
    with config_loader.Config(path_to_dir / utils.ini_name) as config:
        config.cli = parse_cli_arguments()
        logger.debug(f" Parsed arguments: {config.cli}")
    try:
        game.run(config)
    except Exception as err:
        logger.exception(f"Uncaught exception {repr(err)} occurred.")
    logger.debug("Program ended")


if __name__ == "__main__":
    cli_start()
