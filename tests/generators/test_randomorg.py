#!/usr/bin/env python

import time
from absolutris.generators import randomorg


def test_randomorg():
    expected = set((0, 1, 2, 3, 4, 5, 6,))
    actual = set()
    for _ in range(100):
        time.sleep(0.1)
        actual.add(randomorg.pop())
    assert actual == expected


def test_quota():
    assert randomorg.src.check_quota() <= 250000
