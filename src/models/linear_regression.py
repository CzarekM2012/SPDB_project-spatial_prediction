import sys
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path

import numpy as np
from joblib import dump, load
from sklearn.linear_model import LinearRegression

from src.util.data_io import read_data, write_data


class _Commands(Enum):
    TRAIN = "train"
    PREDICT = "predict"


def _parse_command():
    parser = ArgumentParser(
        description="""Train models implementing linear regression algorithm and use them to
        predict values"""
    )
    parser.add_argument(
        "command",
        choices=[command.value for command in _Commands],
        type=str,
        help="Command to execute",
    )
    return parser.parse_args(sys.argv[1:2])


_TRAINED_DIRECTORY = "models"
_TRAINED_PREFIX = "linear_regression_"


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
        '{_TRAINED_DIRECTORY}/{_TRAINED_PREFIX}<data>'""",
    )
    return parser.parse_args(sys.argv[2:])


_PREDICTED_SUFFIX = "_predicted_linear"


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
        t_args.target = Path(_TRAINED_DIRECTORY) / Path(
            f"{_TRAINED_PREFIX}{t_args.data.stem}"
        )
    data = read_data(t_args.data)
    model = train(data)
    dump(model, t_args.target)


def train(data: np.ndarray):
    data_points_indices = np.asarray(np.logical_not(np.isnan(data))).nonzero()
    values = data[data_points_indices]
    data_points_indices = np.transpose(data_points_indices)
    model = LinearRegression()
    model.fit(data_points_indices, values)
    return model


def _predict_subroutine():
    p_args = _parse_predict_params()
    if p_args.target is None:
        p_args.target = p_args.query.with_stem(p_args.query.stem + _PREDICTED_SUFFIX)
    incomplete_data = read_data(p_args.query)
    model: LinearRegression = load(p_args.model)
    filled_data = predict(model, incomplete_data)
    write_data(p_args.target, filled_data)


def predict(model: LinearRegression, incomplete_data: np.ndarray):
    queries_indices = np.asarray(np.isnan(incomplete_data)).nonzero()
    prediction_indices = np.transpose(queries_indices)
    predictions = model.predict(prediction_indices)
    filled_data = incomplete_data.copy()
    filled_data[queries_indices] = predictions
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
