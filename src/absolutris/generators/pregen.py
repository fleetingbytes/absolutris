#!/usr/bin/env python

from __future__ import annotations

import pathlib
import datetime
import requests
import numpy
import io
import logging
from contextlib import contextmanager
from collections import deque
from absolutris import config_loader
from absolutris import utils
from absolutris import errors

# Setup logging:
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


BITS_IN_BYTE = 8
MINO_BIT_LENGTH = 3
IGNORED_BIT_SEQUENCE = 0b111
RANDOM_FILE_BIT_LENGTH = 0x800000


def date_as_str(date: datetime.datetime) -> str:
    """
    Returns today's date in YYYY-MM-DD format
    """
    return date.strftime("%Y-%m-%d")


def file_url(date: datetime.datetime) -> str:
    """
    Returns the URL of today's random bytes archive
    """
    return f"https://archive.random.org/download?file={date_as_str(date)}.bin"


def download_bytes(config: config_loader.Config) -> pathlib.Path:
    """
    Downloads today's pregenerated file of random bits from archive.random.org
    and saves it in the pregen directory
    and returns the pathlib.Path to it.
    """
    pregen_dir = utils.provide_dir(config.path_to_home / "pregen")
    date = datetime.datetime.today()
    target_file = pregen_dir / (date_as_str(date) + ".bin")
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
    url = file_url(date)
    if not target_file.exists():
        response = requests.get(url, headers=headers)
        with open(target_file, mode="wb") as out_file:
            out_file.write(response.content)
    return target_file


@contextmanager
def init_file(file_path: pathlib.Path, bits_used: int) -> tuple[io.BufferedReader, io.BufferedRandom]:
    file = open(file_path, mode="rb")
    pos_file = open(file_path.with_suffix(".pos"), mode="r+b")
    file.seek(bits_used // BITS_IN_BYTE)
    try:
        yield (file, pos_file)
    finally:
        file.close()
        logger.debug(f"{target_file} closed.")
        pos_file.close()
        logger.debug(f"{pos_file} closed.")


def get_mino(file: io.BufferedReader, bits_used: int=0) -> tuple[int, int]:
    """
    Reads from `file` unused bits until they can be mapped to mino.
    returns mino as base 7 integer
    """
    # This loop will repeat until potential_mino will be other than IGNORED_BIT_SEQUENCE (7)
    potential_mino = IGNORED_BIT_SEQUENCE
    while potential_mino == IGNORED_BIT_SEQUENCE:
        byts = file.read(1)
        if byts:
            logger.debug(f"read {byts = }")
            bits_used_in_bytes = bits_used % BITS_IN_BYTE
            logger.debug(f"{bits_used_in_bytes = }")
            usable_bits = BITS_IN_BYTE - bits_used_in_bytes
            logger.debug(f"{usable_bits = }")
            # for one mino we need 3 usable bits. If this byte has less than 3 usable bits, read one more byte
            if usable_bits < MINO_BIT_LENGTH:
                byts += file.read(1)
                if len(byts) < 2:
                    bits_used = RANDOM_FILE_BIT_LENGTH
                    raise errors.DepletedRandomSource(file.name, bits_used)
                usable_bits += BITS_IN_BYTE
                logger.debug(f"read {byts = }")
            int_from_byts = int.from_bytes(byts, byteorder="big", signed=False) & (~((2 ** bits_used_in_bytes - 1) << (len(byts) * BITS_IN_BYTE - bits_used_in_bytes)))
            logger.debug(("{0:0" + str(usable_bits) + "b}").format(int_from_byts))
            potential_mino = int_from_byts >> (usable_bits - MINO_BIT_LENGTH)
            if potential_mino == IGNORED_BIT_SEQUENCE:
                logger.debug("ignoring bits {0:0b}".format(IGNORED_BIT_SEQUENCE))
            else:
                logger.debug(("potential_mino: {0:03b}").format(potential_mino))
            bits_used += MINO_BIT_LENGTH
            logger.debug(f"bits_used increased to {bits_used}")
            file.seek(bits_used // BITS_IN_BYTE)
        else:
            bits_used = RANDOM_FILE_BIT_LENGTH
            raise errors.DepletedRandomSource(file.name, bits_used)
    return (potential_mino, bits_used)


def read_randomness(file: io.BufferedReader, bits_used: int=0, n_minoes: int=0) -> tuple[Deque[int], int]:
    """
    Reads minoes from pregenerated random bytes file until it has read n_minoes.
    Returns a deque of minoes and number of bits used.
    `bits_used` is the total number of bits already read from the file with pregenerated random bytes
    """
    minoes = deque(tuple(None for _ in range(n_minoes)), maxlen=n_minoes)
    logger.debug(minoes)
    while None in minoes:
        (mino, bits_used) = get_mino(file, bits_used=bits_used)
        minoes.append(mino)
        logger.debug(f"minoes: {''.join(tuple(str(mino) for mino in minoes if mino is not None))}")
        logger.debug(f"{bits_used = }")
    return (minoes, bits_used)


if __name__ == "__main__":
    from absolutris import testhelper
    target_file = download_bytes(testhelper.config)
    bits_used = RANDOM_FILE_BIT_LENGTH - 17
    with init_file(target_file, bits_used) as (file, pos_file):
        while True:
            try:
                n_minoes = int(input("How many minoes to read?: "))
            except ValueError as e:
                logger.error(e)
                continue
            if n_minoes == 0:
                break
            else:
                try:
                    (minoes, bits_used) = read_randomness(file, bits_used=bits_used, n_minoes=n_minoes)
                except errors.DepletedRandomSource as e:
                    logger.exception(e)
