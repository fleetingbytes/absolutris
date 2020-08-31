#!/usr/bin/env python
from absolutris.generators import pygen

def test_pygen_stress_pop():
    """
    Tests if this generator can pop 1000 numbers
    """
    expected = set(range(7))
    actual = set()
    for _ in range(1000):
        actual.add(pygen.pop())
    assert expected == actual


def test_pygen_stress_source():
    """
    Tests if this generator can yield 1000 numbers from the source
    """
    expected = set(range(7))
    actual = set()
    src = pygen.source()
    for _ in range(1000):
        actual.add(next(src))
    assert expected == actual

