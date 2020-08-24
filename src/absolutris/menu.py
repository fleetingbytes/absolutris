#!/usr/bin/env python

from __future__ import annotations
import os
import collections
import logging
import pyfiglet


# Setup logging
logger = logging.getLogger(__name__)


class Text_Menu:
    """
    Command prompt menu to debug and play tetris with no GUI.
    """
    def __init__(self) -> None:
        self.figlet = pyfiglet.Figlet(font="drpepper")
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
        for line in self.figlet.renderText("Menu").split("\n"):
            logger.info(line)
        for key, text in options.items():
            logger.info(f"({key}) {text}")


if __name__ == "__main__":
    pass
