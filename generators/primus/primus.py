import pathlib
import numpy
import logging
import logging.config
import logging_conf


#Setup logging
logging.config.dictConfig(logging_conf.dict_config)
logger = logging.getLogger(__name__)


def process_data():
    with open(pathlib.Path("data/primes1.txt"), mode="r", newline="\r\n") as fh:
        # ignore first two lines
        for _ in range(2):
            next(fh)
        for line in fh:
            list_of_strings = line.strip().split()
            # print the last three digits of the base 7 represantation of the primes and concatenate them
            yield ("".join([numpy.base_repr(int(x), base=7)[-3:] for x in list_of_strings]))

if __name__ == "__main__":
    with open(pathlib.Path("processed1.txt"), mode="w") as file:
        file.write("".join(process_data()))
