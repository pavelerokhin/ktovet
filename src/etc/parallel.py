import multiprocessing
import os
import random


def process_in_parallel(data, process_routine, t0, max_pool):
    data = random.sample(data, len(data))

    # Create an atomic integer to keep track of the progress
    manager = multiprocessing.Manager()
    out = manager.list()
    fails = manager.list()

    # Create a process pool with a size of `max_pool`
    with multiprocessing.Pool(processes=max_pool) as pool:
        # Map the data to the process pool and collect the results
        results = [pool.apply_async(process_routine, args=(value, t0, out, fails)) for value in data]

        # Wait for all the tasks to finish and retrieve the results
        for result in results:
            result.get()

    return list(out), list(fails)


def save_in_parallel(data, process_routine, t0, max_pool, download_path):
    data = random.sample(data, len(data))

    # read names of sub folders in download_path
    marker = 0
    if os.path.exists(download_path):
        sub_folders = [int(f.name) for f in os.scandir(download_path) if f.is_dir()]
        marker = max(sub_folders) + 1 if len(sub_folders) > 0 else 0

    # Create an atomic integer to keep track of the progress
    manager = multiprocessing.Manager()
    out = manager.list()
    fails = manager.list()

    # Create a process pool with a size of `max_pool`
    with multiprocessing.Pool(processes=max_pool) as pool:
        # Map the data to the process pool and collect the results
        data = enumerate(data)
        results = [pool.apply_async(process_routine, args=(value, t0, out, fails, download_path, (marker + i))) for i, value in data]

        # Wait for all the tasks to finish and retrieve the results
        for result in results:
            result.get()

    return list(out), list(fails)
