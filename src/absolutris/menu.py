#!/usr/bin/env python

from __future__ import annotations
import os
import collections
import logging


# Setup logging
logger = logging.getLogger(__name__)


class Text_Menu:
    """
    Command prompt menu to debug and play tetris with no GUI.
    """
    def __init__(self) -> None:
        pass
    def wait_key(self) -> str:
        """
        Wait for a key press on the console and return it.
        """
        result = None
        if os.name == 'nt':
            import msvcrt
            result = msvcrt.getch()
        else:
            import termios
            fd = sys.stdin.fileno()
            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)
            try:
                result = sys.stdin.read(1)
            except IOError:
                pass
            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        return str(result, encoding="utf-8").upper()
    def show(self, options: collections.OrderedDict) -> None:
        """
        Renders a command prompt menu for each exrtacted traces file.
        Manages key input and acts accordingly
        """
        for key, text in options.items():
            print(f"({key}) {text}")
        key = self.wait_key()
        try:
            return key
        except ValueError:
            logger.debug(f"Quitting menu")


if __name__ == "__main__":
    pass
