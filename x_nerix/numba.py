#!/usr/bin/python3

import pandas as pd
import numpy as np
from plydata import *
from plydata.tidy import *

df = pd.read_csv("combined.csv")

grouped = (
    df
    >> group_by("irmode", "phase")
    >> summarize(
        duration_sum="sum(duration)",
        duration_count="len(duration)",
        duration_err="np.std(duration)",
        was_cached="sum(was_cached)",
    )
    >> pivot_wider(
        names_from="phase",
        values_from=(
            "duration_sum",
            "duration_count",
            "was_cached",
        ),
        id_cols=("irmode",),
    )
)
print(grouped)
