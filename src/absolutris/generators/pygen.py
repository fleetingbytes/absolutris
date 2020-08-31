#!/usr/bin/env python

import random
from typing import Generator


class Pygen:
    """
    Generates random numbers using the python random module
    """
    def __init__(self, seed=None) -> None:
        self.seeded_random = random.Random(seed)
    def __next__(self) -> int:
        return self.seeded_random.randint(0, 6)
    def source(self) -> Generator[int, None, None]:
        while True:
            yield next(self)


pygen9001 = Pygen(9001)
pop = pygen9001.__next__
source = pygen9001.source


if __name__ == "__main__":
    s = source()
    for _ in range(40):
        print(next(s))
