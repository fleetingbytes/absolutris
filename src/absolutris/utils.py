#!/usr/bin/env python


import logging
import pathlib

# Setup logging
logger = logging.getLogger(__name__)


def provide_dir(dir_name: pathlib.Path) -> pathlib.Path:
    """
    Checks if there is a directory of name `dir_name` in the user home path.
    If not, it will try to create one. 
    """
    directory = pathlib.Path.home() / dir_name
    if directory.exists() and directory.is_dir():
        pass
        # logger.debug(f"Found {str(directory)}")
    else:
        while True:
            try:
                directory.mkdir()
                # logger.info(f"Created {str(directory)}")
                break
            except FileNotFoundError:
                provide_dir(directory.parent)
                provide_dir(directory)
            except FileExistsError:
                logger.debug(f"{directory} already exists")
                break
    return directory


