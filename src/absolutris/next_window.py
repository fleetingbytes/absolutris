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
        result = list()
        for i in range(min(self.length, number)):
            result.append(self.window[i])
        return result
    def next_gen(self) -> Generator[int, None, None]:
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
