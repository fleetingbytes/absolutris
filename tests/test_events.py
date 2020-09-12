#!/usr/bin/env python


import pytest
# for typing
import enum
from typing import TypeVar
# Own modules
from absolutris import events


E = TypeVar("E", enum.IntEnum, enum.IntFlag)
def enum_test(Klass: E, rng: range, raise_error: bool):
    assert Klass(rng.start) == rng.start
    for n in rng:
        assert Klass(n) == n
    if raise_error:
        with pytest.raises(ValueError):
            Klass(rng.stop)
    else:
        assert Klass(rng.stop) == rng.stop


def test_all_events():
    for Klass, rng, raise_error in (
            (events.Next, range(7), True),
            (events.Spawn, range(8), True),
            (events.Soft_Drop_Event, range(2), True),
            (events.Soft_Drop_Type, range(4), True),
            (events.Move, range(8), False),
            (events.Rotate, range(4), True),
            (events.Column, range(13), True),
            (events.Row, range(32), True),
        ):
        enum_test(Klass, rng, raise_error)

