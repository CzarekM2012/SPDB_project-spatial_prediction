from argparse import ArgumentParser
from pathlib import Path
import numpy as np
from pyinterpolate import inverse_distance_weighting
from src.util.data_io import read_data, write_data
from src.util.cli import limited_float

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
        '<data>{_PREDICTED_SUFFIX}'""",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    incomplete_data = read_data(args.query)
    predictions = []
    inverse_distance_weighting()
    is_missing_value = np.isnan(incomplete_data)
    data_points_indices = np.asarray(is_missing_value).nonzero()
    observations = np.transpose(data_points_indices)
    observations[data_points_indices, :] = incomplete_data[data_points_indices]
    queries_indices = np.asarray(is_missing_value).nonzero()
    predictions_indices = np.transpose(queries_indices)
    predictions = inverse_distance_weighting(observations, queries_indices, args.neighbors, args.power)
    incomplete_data[queries_indices] = predictions
    write_data(args.target, incomplete_data)
