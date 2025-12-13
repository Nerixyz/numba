from collections import defaultdict
import os
from pathlib import Path
import pandas as pd
import numpy as np


def read_all_from(thing: str):
    tdir = os.environ.get("IRTEST_OUT", "/tmp/irtest")
    files = os.listdir(f"{tdir}/{thing}")
    calls_per_file = defaultdict(int)
    failed = set()
    frames = []
    for file in files:
        isfail = file.endswith(".fail")
        if not isfail and not file.endswith(".txt"):
            continue
        test = file.removeprefix("irtest-").removesuffix(".fail").removesuffix(".txt")
        if isfail:
            failed.add(test)
            continue
        inner = pd.read_csv(
            f"{tdir}/{thing}/{file}",
            names=[
                "irmode",
                "phase",
                "duration",
                "was_cached",
            ],
        )
        calls_per_file[test] += len(inner)
        frames.append(inner)
    return calls_per_file, failed, frames


def main():
    calls_by_it = {}
    failed_by_it = {}
    frames: list[pd.DataFrame] = []
    for dir in (
        "numba-nocache-0",
        "numba-cache-0",
        "numba-cache-1",
        "irhash-0",
        "irhash-1",
    ):
        calls, failed, dir_frames = read_all_from(dir)
        calls_by_it[dir] = calls
        failed_by_it[dir] = failed
        frames += dir_frames
    df = pd.concat(frames)
    df.to_csv("combined.csv", index=False)

    if not failed_by_it["numba-nocache-0"]:
        print(
            f"WARNING:\n============================================\nFailed in 0: {failed_by_it['numba-nocache-0']}"
        )
    print(failed_by_it)


if __name__ == "__main__":
    main()
