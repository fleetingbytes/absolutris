import numpy
import logging
import logging.config
import logging_conf


#Setup logging
logging.config.dictConfig(logging_conf.dict_config)
logger = logging.getLogger(__name__)

# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/

def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}
    
    # The running integer that's checked for primeness
    q = 2
    
    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            # 
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next 
            # multiples of its witnesses to prepare for larger
            # numbers
            # 
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1

def gen_bags():
    for prime in gen_primes():
        # convert it to base 7:
        prime7 = numpy.base_repr(prime, base=7)
        # return the last digit:
        yield int(prime7[-1], base=7)

generator = gen_bags()

def generate():
    return next(generator)


if __name__ == "primus":
    for _ in range(20000):
        logger.debug(f"{generate()}")
