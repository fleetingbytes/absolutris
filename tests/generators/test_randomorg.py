#!/usr/bin/env python

from absolutris.generators import randomorg

def test_check_quota():
    assert randomorg.check_quota() == 1


def test_randomorg():
    assert randomorg.pop() == 1
