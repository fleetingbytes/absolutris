#!/usr/bin/env python

from typing import Type
from typing import Iterable
from absolutris import gui


def find_gui_classes() -> Iterable[Type[gui.Gui]]:
    """
    Yields all GUI classes found in gui.py.
    """
    for name, item in gui.__dict__.items():
        try:
            if issubclass(item, gui.Gui):
                yield item
        except TypeError:
            continue


def find_gui_instances() -> Iterable[gui.Gui]:
    """
    Yields all instances of a gui class (or a gui subclass) in gui.py.
    """
    for name, item in gui.__dict__.items():
        try:
            if isinstance(item, gui.Gui):
                yield item
        except TypeError:
            continue


def test_gui_classes():
    """
    Checks if a Gui class is usable.
    What makes a Gui class usable?
    """
    for GC in find_gui_classes():
        # Check if it generates instances of Gui
        assert isinstance(GC(), gui.Gui)




if __name__ == "__main__":
    for gc in find_gui_classes():
        print(gc)
    for gi in find_gui_instances():
        print(gi)
