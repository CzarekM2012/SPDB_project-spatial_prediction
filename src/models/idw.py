from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from photutils.utils import ShepardIDWInterpolator

from src.util.cli import limited_float
from src.util.data_io import read_data, write_data

_PREDICTED_SUFFIX = "_predicted_idw"


def _parse_args():
    parser = ArgumentParser(
        description="""Use Inverse Distance Weighting algorithm to predict values"""
    )
    parser.add_argument(
        "-q",
        "--query",
        type=Path,
        required=True,
        help="File containing data with missing values to be predicted",
    )
    parser.add_argument(
        "-p",
        "--power",
        type=limited_float(0.0),
        default=2.0,
        help="""Real positive number. Weights of neighbors of predicted point will be raised to the
        power it specifies.""",
    )
    parser.add_argument(
        "-n",
        "--neighbors",
        type=limited_float(1.0, low_inclusive=True),
        default=5.0,
        help="Positive inteder. Number of closest neighbors used to predict value of a point.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        default=None,
        help=f"""File to save data with missing values filled in using predictions. If omitted,
        results will be saved in the same directory as 'data' under name
        '<data>_<power>_<neighbors>{_PREDICTED_SUFFIX}'""",
    )
    return parser.parse_args()


def predict(incomplete_data: np.ndarray, n_neighbors: int, power: float):
    is_missing = np.isnan(incomplete_data)
    data_points_indices = np.asarray(np.logical_not(is_missing)).nonzero()
    values = incomplete_data[data_points_indices]
    model = ShepardIDWInterpolator(np.array(data_points_indices).T, values)
    missing_values_indices = np.asarray(is_missing).nonzero()
    predictions = model(
        np.array(missing_values_indices).T, n_neighbors=n_neighbors, power=power
    )
    filled_data = incomplete_data.copy()
    filled_data[missing_values_indices] = predictions
    return filled_data


if __name__ == "__main__":
    args = _parse_args()
    args.neighbors = int(args.neighbors)
    if args.target is None:
        integer, fraction = str(args.power).split(".")
        last_nonzero = max([fraction.rfind(digit) for digit in "123456789"])
        power_str = integer + fraction[: last_nonzero + 1]
        args.target = args.query.with_stem(
            f"{args.query.stem}_{power_str}_{args.neighbors}{_PREDICTED_SUFFIX}"
        )

    data = read_data(args.query)
    data = predict(data, args.neighbors, args.power)
    write_data(args.target, data)
