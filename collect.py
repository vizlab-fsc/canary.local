import os
import json
import logging
from glob import glob
from datetime import datetime
from multiprocessing import Pool

logger = logging.getLogger('collector')


def collect(save_dir, items_fn, process_fn, default=dict, save_every=100, jobs=1):
    """convenience wrapper for building out a dataset
    - `save_dir`: directory where to save threads to (as json files)
    - `items_fn`: function to generate a list of arguments to be called by
        `process_fn`, e.g. a list of ids to fetch
    - `process_fn`: function to process an individual item, e.g. fetch a record
    - `default`: function to generate the empty dataset, if `save_file` does
        not exist
    - `save_every`: save the dataset every `save_every` items
    - `jobs`: number of processes to run in parallel
    """
    logger.info('Collecting: {}'.format(datetime.now().isoformat()))

    # assuming thread save files are named by thread id
    thread_files = glob('{}/*.json'.format(save_dir))
    seen = {
        fname.split('/')[-1].replace('.json', ''): fname
        for fname in thread_files
    }
    items = items_fn(seen)
    logger.info('to update: {}'.format(len(items)))

    chunks = [items[i:i+save_every] for i in range(0, len(items), save_every)]
    with Pool(jobs) as p:
        for i, chunk in enumerate(chunks):
            logger.info('chunk: {}/{}'.format(i+1, len(chunks)))
            results = p.starmap(process_fn, chunk)

            logger.info('saving...')
            for key, val in results:
                if val is not None:
                    path = os.path.join(save_dir, '{}.json'.format(key))
                    with open(path, 'w') as f:
                        json.dump(val, f)
            logger.info('saved')
