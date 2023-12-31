import timeit
from pathlib import Path
from subprocess import call

import numpy as np

from src.models.idw import predict as idw_predict
from src.models.kriging import predict as kriging_predict
from src.models.kriging import train as kriging_train
from src.models.linear_regression import predict as linear_regression_predict
from src.models.linear_regression import train as linear_regression_train
from src.util.data import subsample
from src.util.data_io import read_data


def linear_regression_train_factory(samples: np.ndarray):
    def train():
        return linear_regression_train(samples)

    return train


def linear_regression_predict_factory(model, blanks: np.ndarray):
    def predict():
        return linear_regression_predict(model, blanks)

    return predict


def idw_predict_factory(blanks: np.ndarray):
    def predict():
        return idw_predict(blanks, 5, 1)

    return predict


def kriging_train_factory(samples: np.ndarray):
    def train():
        return kriging_train(samples)

    return train


def kriging_predict_factory(model, blanks: np.ndarray):
    def predict():
        return kriging_predict(model, blanks)

    return predict


if __name__ == "__main__":
    try:
        data = read_data(Path("data/processed/poland_DEM/area_elevation_1.asc"))
    except FileNotFoundError:
        try:
            call(["python", "-m", "src.data.poland_dem"])
            data = read_data(Path("data/processed/poland_DEM/area_elevation_1.asc"))
        except FileNotFoundError as error:
            raise RuntimeError(
                """File data/raw/poland_DEM/area_elevation_1.asc, which should be the repository
                is missing"""
            ) from error

    samples_count = (500, 1000, 2000, 4000)
    sampled_datas = [subsample(data, count / data.size) for count in samples_count]
    missing_values_count = (10000, 20000, 40000, 80000)
    incomplete_datas = []
    for count in missing_values_count:
        sampled = subsample(data, count / data.size)
        incomplete_data = np.where(np.isnan(sampled), data, np.nan)
        incomplete_datas.append(incomplete_data)

    print("Linear regression:")
    for count, samples in zip(samples_count, sampled_datas):
        time = timeit.timeit(linear_regression_train_factory(samples), number=10)
        print(f"Training model on {count} samples took: {time}s")
    for count, blanks, samples in zip(
        missing_values_count, incomplete_datas, sampled_datas
    ):
        model = linear_regression_train(samples)
        time = timeit.timeit(
            linear_regression_predict_factory(model, blanks),
            number=10,
        )
        print(f"Predicting {count} missing values took: {time}s")

    print("\nIDW:")
    for count, blanks in zip(missing_values_count, incomplete_datas):
        time = timeit.timeit(idw_predict_factory(blanks))
        print(f"Predicting {count} missing values took: {time}s")

    print("\nKriging:")
    for count, samples in zip(samples_count, sampled_datas):
        time = timeit.timeit(kriging_train_factory(samples), number=10)
        print(f"Training model on {count} samples took: {time}s")
    for count, blanks, samples in zip(
        missing_values_count, incomplete_datas, sampled_datas
    ):
        model = kriging_train(samples)
        time = timeit.timeit(
            kriging_predict_factory(model, blanks),
            number=10,
        )
        print(f"Predicting {count} missing values took: {time}s")
