"""
Generates heatmaps of data, predicted values and their difference
"""
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from src.util.data_io import read_data, write_data
from src.util.data import subsample


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Predict missing values in data using choosen model and generate graphical
        representations"""
    )
    parser.add_argument(
        "-r",
        "--ref",
        required=True,
        type=Path,
        help="File containing reference data to compare predictions with.",
    )
    parser.add_argument(
        "-d",
        "--data",
        type=Path,
        default=None,
        help="""File containing data points to be used for prediction. Will be randomly subsampled
        from reference data if omitted.""",
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        type=Path,
        help="File containing model to be used for predictions",
    )
    parser.add_argument(
        "-s",
        "--save-name",
        dest="save_name",
        type=Path,
        default="heatmaps",
        help="""Name of files that results will be saved in. Files will be created in appropriate
        subdirectories of `reports` top-level directory""",
    )
    return parser.parse_args()


def show_heatmap(ax, data: np.ndarray, title: str, colormap: str = "jet"):
    ax.set_title(title)
    heatmap = ax.imshow(data, cmap=colormap)
    ax.invert_yaxis()
    plt.colorbar(heatmap)


if __name__ == "__main__":
    FIGURES_DIR = Path("reports/figures")
    PREDICTIONS_DIR = Path("reports/predictions")

    args = parse_args()
    ref_data = read_data(args.ref)
    if args.data is None:
        samples = subsample(ref_data, 0.02)
    else:
        samples = read_data(args.data)

    # args.model
    temp_predicted = (
        np.ones_like(ref_data) * ref_data.mean()
    )  # TODO: Load model and use it for prediction
    predictions_filename = args.save_name.with_suffix(".asc")
    write_data(PREDICTIONS_DIR.joinpath(predictions_filename), temp_predicted)

    difference = temp_predicted - ref_data

    fig, axs = plt.subplots(nrows=2, ncols=2)
    fig.tight_layout()
    data_ratio = (samples.size - np.count_nonzero(np.isnan(samples))) / samples.size
    x, y = samples.nonzero()
    axs[0][0].set_title(
        f"Basis of prediction ({data_ratio*100:.2f}% of reference data)"
    )
    plot = axs[0][0].scatter(x, y, s=0.1, c=samples[x, y], cmap="jet")
    plt.colorbar(plot)
    show_heatmap(axs[1][0], ref_data, "Reference data")
    show_heatmap(axs[0][1], temp_predicted, "Predicted data")
    show_heatmap(axs[1][1], difference, "Difference", "bwr")

    figure_filename = args.save_name.with_suffix(".png")
    plt.savefig(FIGURES_DIR.joinpath(figure_filename), bbox_inches="tight")
    plt.show()
