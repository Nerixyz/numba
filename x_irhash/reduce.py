from collections import defaultdict
import os
import pandas as pd
import numpy as np


def read_all_from(thing: str):
    tdir = os.environ.get("IRTEST_OUT", "/tmp/irtest")
    files = os.listdir(f"{tdir}/{thing}")
    calls_per_file = defaultdict(int)
    test_results = []
    frames = []
    for file in files:
        isfail = file.endswith(".fail")
        if not isfail and not file.endswith(".txt"):
            continue
        test = file.removeprefix("irtest-").removesuffix(".fail").removesuffix(".txt")
        if isfail:
            test_results.append((thing, test, False))
            continue
        test_results.append((thing, test, True))
        inner = pd.read_csv(
            f"{tdir}/{thing}/{file}",
            names=[
                "irmode",
                "phase",
                "duration",
                "was_cached",
            ],
            dtype={
                "irmode": str,
                "phase": np.int8,
                "duration": np.float64,
                "was_cached": str,
            },
        )
        calls_per_file[test] += len(inner)
        frames.append(inner)
    test_df = pd.DataFrame(test_results, columns=["irmode", "test", "success"])
    return calls_per_file, test_df, frames


def main():
    calls_by_it = {}
    all_tests: list[pd.DataFrame] = []
    frames: list[pd.DataFrame] = []
    for dir in (
        "numba-nocache-0",
        "numba-cache-0",
        "numba-cache-1",
        "irhash-0",
        "irhash-1",
    ):
        calls, tests, dir_frames = read_all_from(dir)
        calls_by_it[dir] = calls
        all_tests.append(tests)
        frames += dir_frames
    df = pd.concat(frames)
    out_dir = os.environ.get("IRTEST_REDUCE_DIR", "x_irhash")
    combined_out = f"{out_dir}/irtest-combined.csv"
    print(f"Write {combined_out}")
    df.to_csv(combined_out, index=False)

    df = pd.concat(all_tests)
    test_out = f"{out_dir}/irtest-tests.csv"
    print(f"Write {test_out}")

    df.to_csv(test_out, index=False)


if __name__ == "__main__":
    main()
