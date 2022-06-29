import signal
from contextlib import contextmanager

from source.exceptions import TimeoutException


# WARNING: ONLY WORKS ON UNIX SYSTEMS!
@contextmanager
def time_limit(seconds, msg="Timed out!"):
    def signal_handler(signum, frame):
        raise TimeoutException(msg)

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
