#!/usr/bin/env python

"""
This module defines functions and classes which are shared across mutliple pytest modules during testruns
"""


from absolutris import entry
from absolutris import gui
from absolutris import config_loader
from typing import Iterable
from typing import Type
from typing import Union


config_dir = entry.provide_user_dir(entry.dir_name)


# instantiate a configuration:
with config_loader.Config(config_dir / entry.ini_name) as config:
    pass


class Cli:
    """
    Class simulating parsed command line arguments.
    """
    def __init__(self, gui: Union[None, str]="default", verbose: bool=False, stats: bool=False):
        self.gui = gui
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


def uint(bit_length: int, integer: int) -> int:
    """
    Creates an unsigned int
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


if __name__ == "__main__":
    pass
