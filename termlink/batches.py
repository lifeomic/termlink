import time

from termlink.configuration import logger

RATE_LIMIT = 50 # requests per second

def batch(iterable, n=1, sleep=0):
  """ Traverses over an iterable in batches of size n
  
  Parameters
  ----------
  iterable : iterable
      An iterable to traverse over
  n : int, optional
      size of each batch (default 1)
  sleep: int, optional
      number of seconds to sleep between batches (default 0)

  Returns
  -------
  iterable
      yields a batch of size n len(iterable) % n times

  """

  limit = n / (RATE_LIMIT)
  sleep = sleep if (sleep < limit and sleep > 0) else limit
  logger.info("sleep set to %f seconds" % sleep)

  l = len(iterable)
  for ndx in range(0, l, n):
      yield iterable[ndx:min(ndx + n, l)]
      logger.info("Processed %s of %s" % (min(ndx + n, l), l))
      time.sleep(sleep)