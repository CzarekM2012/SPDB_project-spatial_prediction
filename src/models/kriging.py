import sys
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import skgstat as skg
from joblib import dump, load

from src.models.config import MODEL_DIRECTORY
from src.util.data_io import read_data, write_data


class _Commands(Enum):
    TRAIN = "train"
    PREDICT = "predict"


def _parse_command():
    parser = ArgumentParser(
        description="""Train models implementing ordinary kriging algorithm and use them to
        predict values"""
    )
    parser.add_argument(
        "command",
        choices=[command.value for command in _Commands],
        type=str,
        help="Command to execute",
    )
    return parser.parse_args(sys.argv[1:2])


_TRAINED_PREFIX = "kriging_"


def _parse_train_params():
    parser = ArgumentParser()
    parser.prog += " " + _Commands.TRAIN.value
    parser.add_argument(
        "-d",
        "--data",
        type=Path,
        required=True,
        help="File containing data to fit the model",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        default=None,
        help=f"""File to save trained model in. If omitted model will be saved at
        '{MODEL_DIRECTORY}/{_TRAINED_PREFIX}<data>'""",
    )
    parser.add_argument(
        "-s",
        "--show",
        action="store_true",
        default=False,
        help="Display variogram characterizing model",
    )
    return parser.parse_args(sys.argv[2:])


_PREDICTED_SUFFIX = "_predicted_kriging"


def _parse_predict_params():
    parser = ArgumentParser()
    parser.prog += " " + _Commands.TRAIN.value
    parser.add_argument(
        "-m",
        "--model",
        type=Path,
        required=True,
        help="File containing model that will be used for predictions",
    )
    parser.add_argument(
        "-q",
        "--query",
        type=Path,
        required=True,
        help="File containing data with missing values to be predicted",
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
    return parser.parse_args(sys.argv[2:])


def _train_subroutine():
    t_args = _parse_train_params()
    if t_args.target is None:
        t_args.target = MODEL_DIRECTORY / Path(f"{_TRAINED_PREFIX}{t_args.data.stem}")
    data = read_data(t_args.data)
    model = train(data)
    if t_args.show:
        model.plot(show=False)
        plt.show()
    dump(model, t_args.target)


def train(data: np.ndarray):
    data_points_indices = np.asarray(np.logical_not(np.isnan(data))).nonzero()
    values = data[data_points_indices]
    data_points_indices = np.transpose(data_points_indices)
    model = skg.Variogram(data_points_indices, values)
    return model


def _predict_subroutine():
    p_args = _parse_predict_params()
    if p_args.target is None:
        p_args.target = p_args.query.with_stem(p_args.query.stem + _PREDICTED_SUFFIX)
    incomplete_data = read_data(p_args.query)
    model: skg.Variogram = load(p_args.model)
    filled_data = predict(model, incomplete_data)
    write_data(p_args.target, filled_data)


def predict(model: skg.Variogram, incomplete_data: np.ndarray):
    y, x = np.asarray(np.isnan(incomplete_data)).nonzero()
    kriging = skg.OrdinaryKriging(model)
    filled_data = incomplete_data.copy()
    queries_count = x.size
    batch_size = 2**10 * 4
    start = 0
    for stop in range(batch_size, queries_count, batch_size):
        y_chunk = y[start:stop]
        x_chunk = x[start:stop]
        start = stop
        predictions = kriging.transform(y_chunk, x_chunk)
        filled_data[y_chunk, x_chunk] = predictions
    y_chunk = y[start:]
    x_chunk = x[start:]
    predictions = kriging.transform(y_chunk, x_chunk)
    filled_data[y_chunk, x_chunk] = predictions
    return filled_data


if __name__ == "__main__":
    args = _parse_command()
    match args.command:
        case _Commands.TRAIN.value:
            _train_subroutine()
        case _Commands.PREDICT.value:
            _predict_subroutine()
        case _:
            print("Unknown command")
            sys.exit(1)
