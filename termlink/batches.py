"""A utility for iterating in batches.

This module provides utility methods for iterating over iterables in batches.
"""

import time

from termlink.configuration import Config

configuration = Config()
logger = configuration.logger

RATE_LIMIT = 50  # requests per second


def batch(iterable, n=1, sleep=0):
    """
    Traverses over an iterable in batches of size n sleeping :sleep: seconds
    between batches.

    Args:
        iterable:   An iterable
        n:          Size of each batch
        sleep:      Number of seconds to sleep between batches

    Returns:
        For each batch, yields a batch of size n, len(iterable) % n times
    """

    limit = n / (RATE_LIMIT)
    sleep = sleep if 0 < sleep < limit else limit
    logger.info("sleep set to %f seconds", sleep)

    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]
        logger.info("Processed %s of %s", min(ndx + n, l), l)
        time.sleep(sleep)
