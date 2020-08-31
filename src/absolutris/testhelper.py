#!/usr/bin/env python

"""
This module defines functions and classes which are shared across mutliple pytest modules during testruns
"""

import pathlib
from absolutris import utils
from absolutris import gui
from absolutris import plans
from absolutris import config_loader
from typing import Iterable
from typing import Type
from typing import Union


config_dir = utils.provide_dir()


# instantiate a configuration:
with config_loader.Config(config_dir / utils.ini_name) as config:
    pass


class Cli:
    """
    Class simulating parsed command line arguments.
    """
    def __init__(self, 
                 download: bool=False, 
                 gui: Union[None, str]="default", 
                 plan: Union[None, str]="default", 
                 verbose: bool=False, 
                 stats: bool=False,
            ):
        self.download = download
        self.gui = gui
        self.plan = plan
        self.verbose = verbose
        self.stats = stats


def find_gui_classes() -> Iterable[Type[gui.Gui]]:
    """
    Yields all GUI classes found in gui.py.
    """
    for name, item in gui.__dict__.items():
        try:
            if issubclass(item, gui.Gui):
                yield name, item
        except TypeError:
            continue


def find_gui_instances() -> Iterable[gui.Gui]:
    """
    Yields all instances of a gui class (or a gui subclass) in gui.py.
    """
    for name, item in gui.__dict__.items():
        try:
            if isinstance(item, gui.Gui):
                yield name, item
        except TypeError:
            continue


def find_plan_classes() -> Iterable[Type[plans.Plan]]:
    """
    Yields all Plan classes found in plans.py.
    """
    for name, item in plans.__dict__.items():
        try:
            if issubclass(item, plans.Plan):
                yield name, item
        except TypeError:
            continue


def find_plan_instances() -> Iterable[plans.Plan]:
    """
    Yields all instances of a Plan class (or a Plan subclass) in plans.py.
    """
    for name, item in plans.__dict__.items():
        try:
            if isinstance(item, plans.Plan):
                yield name, item
        except TypeError:
            continue


def uint(bit_length: int, integer: int) -> int:
    """
    Interprets any integer as an unsigned integer of the given bit length.
    Returns the integer's positive two's complement.
    It mimics the uint* types of classical programming languages, 
    e.g. to convert i: int = -13 to uint8, one calls:
        uint(8, -13)
    The result will be 243. (Consequentially, that uint(8, 243) also returns 243).
    """
    if bit_length < 1:
        raise errors.UnsignedIntegerBitLength(f"Bit length must be at least 1")
    if integer >= 0:
        # result = int("{0:0b}".format(integer), base=2)
        if int.bit_length(integer) > bit_length:
            raise errors.UnsignedIntegerOverflow(f"{integer} is too big for {bit_length} bits")
        return integer
    else:
        # return int(("{0:0" + str(bit_length) + "b}").format(~integer ^ (2 ** bit_length - 1)), base=2)
        if integer < -(2 ** bit_length) // 2:
            raise errors.UnsignedIntegerOverflow(f"{integer} is too small for {bit_length} bits")
        return ~integer ^ (2 ** bit_length - 1)


def in_bitfield(integer: int, bitfield: int) -> bool:
    """
    Checks if the integer can be expressed by the given bit field.
    """
    return (integer | bitfield) == bitfield


def pygame_wrapper(coro):
    yield from coro


def create_random_bytes_file(byts: bytes) -> pathlib.Path:
    """
    Creates the file `test_bytes.bin` in user's home/absolutris.
    Writes the given bytes into it and returns the path to this file
    """
    file_path = utils.provide_dir() / "test_bytes.bin"
    with open(file_path, mode="wb") as file:
        file.write(byts)
    return file_path


if __name__ == "__main__":
    pass
