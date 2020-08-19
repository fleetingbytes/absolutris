#!/usr/bin/env python

import pathlib


def bits(n_minos: int) -> int:
    """
    Says how many bits are necessary to store the sequence of n minos
    """
    return int(str(6) * n_minos, base=7).bit_length()


def readfile(name: str) -> bytes:
    """
    reads bytes from a file and returns a list of integers which represents minoes
    recorded in that file
    """
    with open(pathlib.Path.cwd() / name, mode="rb") as file:
        b = file.read()
        return b


def number_to_base(n: int, b: int) -> list:
    """
    https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    """
    if n == 0:
        return [0]
    digits = list()
    while n:
        digits.append(int(n % b))
        n = n // b
    digits.reverse()
    return digits


if __name__ == "__main__":
    # for n in range(1, 60000):
        # b = bits(n)
        # if b % 8 == 0:
            # print(f"{n} minoes can be stored in {b // 8} bytes. Or {b // 3} octal digits.")
    b = readfile("bytes.bin")
    i = int.from_bytes(b, byteorder="little", signed=False)
    minoes = number_to_base(i, 7)
