#!/usr/bin/env python

import time
from absolutris.generators import randomorg


def test_randomorg_pop():
    expected = set(range(7))
    actual = set()
    for _ in range(100):
        time.sleep(0.1)
        actual.add(randomorg.pop())
    assert actual == expected


def test_randomorg_source():
    expected = set(range(7))
    actual = set()
    s = randomorg.source()
    for _ in range(100):
        time.sleep(0.1)
        actual.add(next(s))
    assert actual == expected


def test_quota():
    assert randomorg.src.check_quota() <= 250000
