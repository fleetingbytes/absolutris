#!/usr/bin/env python
from absolutris.generators import pygen

def test_pygen_stress():
    """
    Tests if this generator can generate 1000 numbers
    """
    expected = set((0, 1, 2, 3, 4, 5, 6))
    actual = set()
    for _ in range(1000):
        actual.add(pygen.pop())
    assert expected == actual
