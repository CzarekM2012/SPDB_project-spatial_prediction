import math
import numpy as np


def subsample(data: np.ndarray, ratio: float):
    if not 0 < ratio < 1:
        raise ValueError("Ratio needs to be between 0 and 1")
    subsampled = np.full_like(data, np.nan)
    max_row_index = data.shape[0] - 1
    max_col_index = data.shape[1] - 1
    samples_count = math.floor(data.size * ratio)
    while samples_count > 0:
        x = np.random.randint(0, max_col_index)
        y = np.random.randint(0, max_row_index)
        if np.isnan(subsampled[y, x]):
            subsampled[y, x] = data[y, x]
            samples_count -= 1
    return subsampled
