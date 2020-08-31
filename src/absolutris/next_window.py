#!/usr/bin/env python


import logging
import collections
from typing import Generator


# Setup logging
logger = logging.getLogger(__name__)


DEFAULT_WINDOW_LENGTH = 1


class Next_Window:
    def __init__(self, source: Generator[int, None, None], length: int=DEFAULT_WINDOW_LENGTH):
        self.source = source
        self.length = length
        self.window = collections.deque(tuple(next(self.source) for _ in range(self.length)))
    def next_gen(self) -> Generator[int, None, None]:
        while self.window:
            to_spawn = self.window.popleft()
            try:
                self.window.append(next(self.source))
            except StopIteration as err:
                logger.exception(err)
            yield to_spawn



if __name__ == "__main__":
    pass
