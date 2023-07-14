import time

from ..etc.dump import dump_stage, read_dump
from ..etc.output import output
from ..etc.utils import GREEN, HEADER, RED, WHITE

MAX_ATTEMPTS = 3


def stage(data=None, i=0, t0=time.time(), max_pool=10, store_partial=True):
    print(f"input: {len(data)} items to process")

    if i >= MAX_ATTEMPTS:
        dump_pages, dump_fails = read_dump(1)
        print(f"{RED}maximum number of attempts ({MAX_ATTEMPTS}) exceeded{WHITE}, process {len(dump_pages)} pages loaded from memory")
        return dump_pages

    pages, fails = process_previews(previews=data, t0=t0, max_pool=max_pool)
    if fails:
        dump_stage(pages, fails, stage=1)
        i += 1
        return stage(fails, i, t0, max_pool)

    dump_pages, dump_fails = read_dump(1)
    pages.extend(dump_pages)
    fails.extend(dump_fails)

    print(f"{GREEN}{len(pages)}{WHITE} items processed, {round(time.time() - t0, 2)}s")

    if store_partial:
        output(pages, fails, 1)

    return pages
