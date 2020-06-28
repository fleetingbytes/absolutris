#!/usr/bin/env python
from absolutris.generators import pygen

def test_pygen_stress():
    """
    Tests if this generator can generate 1000 numbers
    """
    gen = pygen.Pygen()
    l = list([next(gen) for _ in range(1000)])
    assert len(l) == 1000
    s = set(l)
    assert s == set([0, 1, 2, 3, 4, 5, 6])

