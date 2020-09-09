#!/usr/bin/env python


from absolutris import events


def test_next():
    assert events.Next(0) == 0
    for n in range(1, 7):
        assert events.Next(n) == n
