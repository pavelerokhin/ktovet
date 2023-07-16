import time

from ..etc.dump import dump_stage, read_dump
from ..etc.output import output
from ..etc.utils import GREEN, HEADER, RED, WHITE


MAX_ATTEMPTS = 3
MAX_POOL = 10
STORE_PARTIAL = True


def stage(data=None, schema=None, i=0, t0=time.time()):
    print(f"input: {len(data)} items to process")

    if not schema:
        raise ValueError("schema is not defined")

    stage_id = schema["id"]
    if i >= MAX_ATTEMPTS:
        dump_success, dump_fails = read_dump(stage_id)
        print(f"{RED}maximum number of attempts ({MAX_ATTEMPTS}) exceeded{WHITE}, process {len(dump_success)} items loaded from memory")
        return dump_success

    actions = schema["actions"]

    success, fails = actions(data=data, t0=t0, max_pool=MAX_POOL)
    if fails:
        dump_stage(success, fails, stage=stage_id)
        i += 1
        return stage(fails, schema, i, t0)

    dump_success, dump_fails = read_dump(stage_id)
    success.extend(dump_success)
    fails.extend(dump_fails)

    print(f"{GREEN}{len(success)}{WHITE} items processed, {round(time.time() - t0, 2)}s")

    if STORE_PARTIAL:
        output(success, fails, stage_id)

    return success
