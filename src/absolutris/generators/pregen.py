#!/usr/bin/env python


"""
  _____   ______ _______  ______ _______ __   _
 |_____] |_____/ |______ |  ____ |______ | \  |
 |       |    \_ |______ |_____| |______ |  \_|

Uses pregenerated random binary from archive.random.org
to create truly random tetrominoes.
"""


from __future__ import annotations

import pathlib
import datetime
import requests
import io
import logging
from contextlib import contextmanager
from collections import deque
from absolutris import utils
from absolutris import errors

# Setup logging:
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


BITS_IN_BYTE = 8
MINO_BIT_LENGTH = 3
IGNORED_BIT_SEQUENCE = 0b111
RANDOM_FILE_BIT_LENGTH = 0x800000


class Random_File_Handler:
    """
    Reads from a random bytes file.
    Creates a corresponding .pos file which tracks how many bits
    from the random bytes file have already been read.

    Has to be initialized with `buffer_length` >= 1.
    """
    def __init__(self, file_path: pathlib.Path, buffer_length: int=50) -> None:
        self.random_file = file_path
        if buffer_length < 1:
            raise ValueError("Random_File_Handler needs a buffer_length >= 1")
        else:
            self.buffer_length = buffer_length
        self.refill_limit = self.buffer_length // 2
        self.buffer = deque(tuple(None for _ in range(self.buffer_length)), maxlen=self.buffer_length)
        self.fill_buffer(self.buffer_length)
    @contextmanager
    def init_file(self, file_path: pathlib.Path) -> tuple[io.BufferedReader, io.BufferedRandom, int]:
        """
        Creates two filehandles. One for the file with random bytes (`file`), 
        another for a file where it tracks how many bits from the random bytes file have already been used (`pos_file`).
        Returns the two file handles and the number of bits which have already been used from the random bytes file.
        """
        file = open(file_path, mode="rb")
        pos_file_path = file_path.with_suffix(".pos")
        pos_file_path.touch(mode=0o666, exist_ok=True)
        with open(pos_file_path, mode="r+b") as pf:
            bits_used = int.from_bytes(pf.read(), byteorder="big", signed=False)
        pos_file = open(pos_file_path, mode="r+b")
        file.seek(bits_used // BITS_IN_BYTE)
        try:
            yield (file, pos_file, bits_used)
        finally:
            file.close()
            logger.debug(f"{file.name} closed.")
            pos_file.close()
            logger.debug(f"{pos_file.name} closed.")
    def write_position(self, pos_file: io.BufferedRandom, bits_used: int) -> None:
        """
        Write the number of used bits to the position file `pos_file`.
        Returns the cursor to the beginning of the file for next access.
        """
        pos_file.write(bits_used.to_bytes(length=RANDOM_FILE_BIT_LENGTH.bit_length() // BITS_IN_BYTE, byteorder="big", signed=False))
        pos_file.seek(0)
        logger.debug(f"{bits_used = } written to {pos_file.name}")
    def get_mino(self, file: io.BufferedReader, bits_used: int=0) -> tuple[int, int]:
        """
        Reads from `file` unused bits until they can be mapped to mino.
        `file` is a filehandle for reading bytes from a file containing pregenerated random bytes.
        `bits_used` is the number of bits which were already read from the beginning of the file
            should be skipped before reading any further bits.
        Returns the tuple(mino, bits_used)
            where `mino` is a single base 7 integer,
            and `bits_used` is an updated value of bits used.
        The file can only be read byte by byte. Bits from the bytes are used from the MSB to LSB.
        If the byte has less bits left than is necessary to compute a mino, an additional byte is
        read, (`n_bytes_to_read`).
        The used bits are masked away and ignored (see the formula for `int_from_byts`).
        """ 
        # This loop will repeat until potential_mino will be other than IGNORED_BIT_SEQUENCE (7)
        potential_mino = IGNORED_BIT_SEQUENCE
        while potential_mino == IGNORED_BIT_SEQUENCE:
            bits_used_in_bytes = bits_used % BITS_IN_BYTE
            logger.debug(f"{bits_used_in_bytes = }")
            usable_bits = BITS_IN_BYTE - bits_used_in_bytes
            logger.debug(f"{usable_bits = }")
            # for one mino we need 3 usable bits. If this byte has less than 3 usable bits, read one more byte
            if usable_bits < MINO_BIT_LENGTH:
                n_bytes_to_read = 2
                usable_bits += BITS_IN_BYTE
            else:
                n_bytes_to_read = 1
            byts = file.read(n_bytes_to_read)
            if len(byts) < n_bytes_to_read:
                bits_used = RANDOM_FILE_BIT_LENGTH
                raise errors.RandomSourceDepleted(file.name, bits_used)
            logger.debug(f"read {byts = }")
            int_from_byts = int.from_bytes(byts, byteorder="big", signed=False) & (~((2 ** bits_used_in_bytes - 1) << (len(byts) * BITS_IN_BYTE - bits_used_in_bytes)))
            logger.debug(("{0:0" + str(usable_bits) + "b}").format(int_from_byts))
            potential_mino = int_from_byts >> (usable_bits - MINO_BIT_LENGTH)
            if potential_mino == IGNORED_BIT_SEQUENCE:
                logger.debug("ignoring bits {0:0b}".format(IGNORED_BIT_SEQUENCE))
            else:
                logger.debug(("potential_mino: {0:0" + MINO_BIT_LENGTH +"b}").format(potential_mino))
            bits_used += MINO_BIT_LENGTH
            logger.debug(f"bits_used increased to {bits_used}")
            file.seek(bits_used // BITS_IN_BYTE)
        return (potential_mino, bits_used)
    def read_randomness(self, file: io.BufferedReader, bits_used: int=0, n_minoes: int=0) -> tuple[Deque[int], int]:
        """
        Reads minoes from pregenerated random bytes file until it has read n_minoes.
        Returns a deque of minoes and number of bits used.
        `bits_used` is the total number of bits already read from the file with pregenerated random bytes
        """
        minoes = deque(tuple(None for _ in range(n_minoes)), maxlen=n_minoes)
        logger.debug(minoes)
        while None in minoes:
            try:
                (mino, bits_used) = self.get_mino(file, bits_used=bits_used)
                minoes.append(mino)
            except errors.RandomSourceDepleted as err:
                while None in minoes:
                    minoes.remove(None)
                logger.warning(f"{file.name} is depleted!")
                bits_used = RANDOM_FILE_BIT_LENGTH
        logger.debug(f"minoes: {''.join(tuple(str(mino) for mino in minoes if mino is not None))}")
        logger.debug(f"{bits_used = }")
        return (minoes, bits_used)
    def fill_buffer(self, n_minoes) -> None:
        """
        Refills the buffer of minoes.
        Minoes are buffered to avoid too frequent file accesses to the
        random bytes file and the position file.
        """
        with self.init_file(self.random_file) as (file, pos_file, bits_used):
            logger.debug("Buffering random minoes")
            (minoes, updated_bits_used) = self.read_randomness(file, bits_used=bits_used, n_minoes=n_minoes)
            self.buffer.extend(minoes)
            self.write_position(pos_file, updated_bits_used)
    def pop(self) -> None:
        """
        Returns the left-most mino in self.buffer.
        Replenishes the buffer if it holds less minoes than self.refill_limit.
        Raises errors.RandomSourceDepleted when poping from an empty buffer.
        """
        try:
            if len(self.buffer) <= self.refill_limit:
                self.fill_buffer(self.buffer_length - self.refill_limit)
            return self.buffer.popleft()
        except IndexError:
            raise errors.RandomSourceDepleted(self.random_file.name, RANDOM_FILE_BIT_LENGTH)


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


def download_bytes() -> pathlib.Path:
    """
    Downloads today's pregenerated file of random bits from archive.random.org
    and saves it in the pregen directory
    and returns the pathlib.Path to it.
    """
    pregen_dir = utils.provide_dir() / "pregen"
    date = datetime.datetime.today()
    target_file = pregen_dir / (date_as_str(date) + ".bin")
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
    url = file_url(date)
    if not target_file.exists():
        response = requests.get(url, headers=headers)
        with open(target_file, mode="wb") as out_file:
            out_file.write(response.content)
    return target_file


rfh = Random_File_Handler(download_bytes(), buffer_length=10)
pop = rfh.pop


if __name__ == "__main__":
    with open(utils.provide_dir() / "pregen" / "2020-08-23.pos", mode="wb") as pos_file:
        pos_file.write((RANDOM_FILE_BIT_LENGTH - 180).to_bytes(length=MINO_BIT_LENGTH, byteorder="big", signed=False))
    rfh = Random_File_Handler(download_bytes(), buffer_length=50)
    pop = rfh.pop
