import math
import numpy as np


def subsample(data: np.ndarray, ratio: float, seed: int = None):
    if not 0 < ratio < 1:
        raise ValueError("Ratio needs to be between 0 and 1")
    subsampled = np.full_like(data, np.nan)
    samples_count = math.floor(data.size * ratio)
    rng = np.random.default_rng(seed)
    while samples_count > 0:
        x = rng.integers(0, data.shape[1])  # data.shape[1] - number of columns
        y = rng.integers(0, data.shape[0])  # data.shape[0] - number of rows
        if np.isnan(subsampled[y, x]):
            subsampled[y, x] = data[y, x]
            samples_count -= 1
    return subsampled
