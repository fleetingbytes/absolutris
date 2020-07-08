#!/usr/bin/env python
import random
from typing import NoReturn


class Pygen:
    """
    Generates random numbers using the python random module
    """
    def __init__(self, seed=None) -> NoReturn:
        self.seeded_random = random.Random(seed)
    def __next__(self) -> int:
        return self.seeded_random.randint(0, 6)


pygen9001 = Pygen(9001)
pop = pygen9001.__next__


if __name__ == "__main__":
    for _ in range(10):
        print(next(pygen9001))
