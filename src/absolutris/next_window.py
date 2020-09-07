#!/usr/bin/env python

import logging
import collections
from typing import Generator


# Setup logging
logger = logging.getLogger(__name__)


DEFAULT_WINDOW_LENGTH = 1


class Next_Window:
    """
    Class for the Next Windows showing upcoming pieces.
    `source` can be either one of the random generators or a packer.
             Either one of them is a Generator[int, None, None]
    `length` is the number of pieces shown in this window. Please note
             that Absolutris GUIs have a limited capability of showing
             next pieces. In the end it's the GUIs decision how many upcoming
             pieces will be shown. 
    `spawn` is a generator which yields next tetrominoes and refills the Next Window buffer.
    """
    def __init__(self, source: Generator[int, None, None], length: int=DEFAULT_WINDOW_LENGTH):
        self.source = source
        self.length = length
        if self.length > 0:
            self.window = collections.deque(tuple(next(self.source) for _ in range(self.length)))
        else:
            self.window = collections.deque(tuple(next(self.source) for _ in range(DEFAULT_WINDOW_LENGTH)))
            self.length = 0
        self.spawn = self.next_gen()
    def show(self, number: int) -> list:
        """
        The length of the Next Window is defined when Next_Window is instantiated, 
        but the GUI also defines its own length of Next Window.
        When the GUI wants to show a `number` of pieces from the next window,
            it calls next_window.show(number). This function decides what number
            of pieces will be actually shown by min(self.length, number).
        This makes sure that when the instance of next_window has a lot of pieces,
        but GUI wants to show only 1 or even 0, it gets only this many.
        Also, vice versa, if the next_window has room only for 1 piece but the GUI
        wants to show 7, this function still returns only 1.
        """
        result = list()
        for i in range(min(self.length, number)):
            result.append(self.window[i])
        return result
    def next_gen(self) -> Generator[int, None, None]:
        """
        Yields the next tetromino from next window to the Game and refills `self.window`
        with the next piece from `self.source`.

        When the Game wants to spawn a new piece on the playfield, it advances this generator.
        However, it is not as simple as popping and yielding the left value from the deque `self.window`
        and then refilling the deque with another tetromino from self.source.
        Such simple solution would leave us with self.window not being filled up with the next tetromino
        until this generator is advanced again later. We therefore popleft to remember what is to be spawned, 
        refill the deque (unless source is depleted), and then yield what is to be spawned.
        """
        while self.window:
            to_spawn = self.window.popleft()
            try:
                self.window.append(next(self.source))
            except StopIteration as err:
                logger.exception(err)
                raise
            yield to_spawn
    def __next__(self) -> int:
         return next(self.spawn)


if __name__ == "__main__":
    # from absolutris.generators import pregen as src
    # nw = Next_Window(source=src.source(), length=3)
    pass
