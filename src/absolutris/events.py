#!/usr/bin/env python

import enum

@enum.unique
class Spawn(enum.IntFlag):
    T = 0b000
    J = 0b001
    Z = 0b010
    O = 0b011
    S = 0b100
    L = 0b101
    I = 0b110
    MOVE_CURRENT = 0b111


class Move(enum.IntFlag):
    ROW = 0b100
    COLUMN = 0b010
    ROTATE = 0b001


class Rotate(enum.IntEnum):
    NORTH = 0b00
    WEST = 0b01
    SOUTH = 0b10
    EAST = 0b11


class Column(enum.IntEnum):
    Q = 0
    A = 1
    W = 2
    S = 3
    E = 4
    D = 5
    R = 6
    F = 7
    T = 8
    G = 9
    Y = 10
    H = 11
    U = 12


class Row(enum.IntEnum):
    ROW32 = 31
    ROW31 = 30
    ROW30 = 29
    ROW29 = 28
    ROW28 = 27
    ROW27 = 26
    ROW26 = 25
    ROW25 = 24
    ROW24 = 23
    ROW23 = 22
    ROW22 = 21
    ROW21 = 20
    ROW20 = 19
    ROW19 = 18
    ROW18 = 17
    ROW17 = 16
    ROW16 = 15
    ROW15 = 14
    ROW14 = 13
    ROW13 = 12
    ROW12 = 11
    ROW11 = 10
    ROW10 = 9
    ROW9 = 8
    ROW8 = 7
    ROW7 = 6
    ROW6 = 5
    ROW5 = 4
    ROW4 = 3
    ROW3 = 2
    ROW2 = 1
    ROW1 = 0


if __name__ == "__main__":
    pass


if __name__ == "__main__":
    pass
