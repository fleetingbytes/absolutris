#!/usr/bin/env python


class Gui:
    """
    Class for GUIs of Absolutris.
    """
    def __init__(self, flags=0, playfield_width=10):
        self.flags = flags
        self.playfield_width = playfield_width


class Malicious(Gui):
    def __init__(self):
        pass


default = Gui()
debug = Gui(flags=32, playfield_width=11)
debug.flags="asdf"

m = Malicious()


if __name__ == "__main__":
    pass
