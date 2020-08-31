#!/usr/bin/env python
from rdoclient import RandomOrgClient
from collections import deque
import time
from typing import List
from typing import Deque
from typing import Generator
from queue import Empty
import logging


# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# API key will be provided later by config
api_key = "63436b3d-408f-4593-a857-5bb1a4ce026b"


class RandomSource:
    """
    Implementation of a random rource based on random.org
    """
    def __init__(self, api_key):
        self._client = RandomOrgClient(api_key, blocking_timeout=3600, http_timeout=30)
        self._cache_length = 20
        self._source = self._client.create_integer_cache(self._cache_length, 0, 6)
        while True:
            try:
                self.buffer = deque(self._source.get(), self._cache_length * 2)
                break
            except Empty as e:
                logger.debug("q empty")
    def check_quota(self) -> int:
        return self._client.get_bits_left()
    def pop(self) -> int:
        if len(self.buffer) <= self._cache_length:
            logging.debug("extending buffer")
            self.buffer.extend(self._source.get())
        try:
            result = self.buffer.popleft()
        except IndexError:
            self.buffer = deque(self._source.get(), self._cache_length)
            result = self.buffer.popleft()
        logger.debug(f"popping {result}")
        return result
    def source(self) -> Generator[int, None, None]:
        while True:
            yield self.pop()


src = RandomSource(api_key)
pop = src.pop
source = src.source


if __name__ == "__main__":
    s = source()
    while True:
        number = next(s)
        print(number)
        logger.debug(f"{number}, quota: {src.check_quota()}")
        time.sleep(0.1)
