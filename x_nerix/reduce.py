import os
from pathlib import Path
import pandas as pd
import numpy as np


def main():
    files = os.listdir("/tmp/irtest")
    frames: list[pd.DataFrame] = []
    for file in files:
        if not file.endswith(".txt"):
            continue
        test = file.removeprefix("irtest-").removesuffix(".txt")
        inner = pd.read_csv(
            f"/tmp/irtest/{file}",
            names=["irmode", "phase", "duration", "was_cached", "had_typing_error"],
        )
        inner["test"] = test
        frames.append(inner)
        # print(inner)
        # break
    df = pd.concat(frames)
    df.to_csv("combined.csv", index=False)
    df2 = df.groupby(["irmode", "phase", "test"]).agg(
        {"duration": "mean", "was_cached": list}
    )
    df2.to_csv("combined2.csv")
    # df2["irmode"]
    df2 = pd.read_csv("combined2.csv")

    idur = df2[(df2["irmode"] == "irhash") & (df2["phase"] == 1)]["duration"].mean()
    ndur = df2[df2["irmode"] == "numba-nocache"]["duration"].mean()
    print(idur)
    print(ndur)
    print((ndur - idur) / ndur)


if __name__ == "__main__":
    main()
