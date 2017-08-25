import os
import sys
import fcntl
import logging
from time import sleep
from domains import chan
from collect import collect
from functools import partial
from datetime import datetime
from raven import Client


here = os.path.dirname(__file__)


def count(save_dir):
    return len(os.listdir(save_dir))


def rel(fname):
    return os.path.join(here, 'data', fname)


def record_count(name):
    with open(rel('_{}_updates.txt'.format(name)), 'a') as f:
        f.write('{}->{}\n'.format(
            datetime.now().isoformat(),
            count(rel(name))))


def acquire_lock(name):
    try:
        lock = open('/tmp/{}.lock'.format(name), 'w+')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('another slurper for "{}" is running, exiting'.format(name))
        sys.exit(1)


if __name__ == '__main__':
    INTERVAL = 5 * 60
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    name = sys.argv[1]
    acquire_lock(name)

    try:
        dsn = open(os.path.expanduser('~/.sentry_dsn'), 'r').read().strip()
        client = Client(dsn)
    except FileNotFoundError:
        client = None

    while True:
        try:
            if name == 'pol':
                pol = chan.four('pol')
                collect(
                    rel('pol'),
                    partial(chan.threads_to_update, pol),
                    partial(chan.get_thread, pol))
                record_count('pol')
            sleep(INTERVAL)
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            logger.exception(e)
            if client is not None:
                client.captureException()
            else:
                raise
