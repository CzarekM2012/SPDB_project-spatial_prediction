from pathlib import Path

import numpy as np

from src.util.data_io import write_data


def waves(
    shape: tuple[int, int],
    amplitude_ranges: tuple[tuple[float, float], tuple[float, float]] = (
        (10.0, 100.0),
        (10.0, 100.0),
    ),
    min_val: float = 100.0,
):
    row = np.sin(np.arange(shape[1]) * np.pi / 180.0)
    column = np.sin(np.arange(shape[0]) * np.pi / 180.0)
    row *= np.linspace(amplitude_ranges[1][0], amplitude_ranges[1][1], shape[1])
    column *= np.linspace(amplitude_ranges[0][0], amplitude_ranges[0][1], shape[0])
    data = row + column[:, np.newaxis]
    shift = min_val - data.min()
    data += shift
    return data


if __name__ == "__main__":
    GENERATED_DIR = Path("data/processed/generated")
    if not GENERATED_DIR.is_dir():
        GENERATED_DIR.mkdir()
    write_data(GENERATED_DIR.joinpath("waves.asc"), waves((360, 360)))
