"""
Generates heatmaps of data, predicted values and their difference
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.util.data_io import read_data

_TARGET_SUFFIX = "_comparison"


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Generate graphical comparison of data"""
    )
    parser.add_argument(
        "-r",
        "--reference",
        required=True,
        type=Path,
        help="File containing reference data to compare predictions with",
    )
    parser.add_argument(
        "-s",
        "--samples",
        required=True,
        type=Path,
        help="""File containing data samples on the basis of which predictions were made""",
    )
    parser.add_argument(
        "-p",
        "--predictions",
        required=True,
        type=Path,
        help="File containing predictions",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        default=None,
        help=f"""File to save figure in. If omitted it will be saved in 'reports/figures'
        directory '<reference>_<predictions>{_TARGET_SUFFIX}""",
    )
    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        default=False,
        help="Display generated figure",
    )
    return parser.parse_args()


def show_heatmap(
    ax, data: np.ndarray, title: str, colormap: str = "jet", vmin=None, vmax=None
):
    ax.set_title(title)
    heatmap = ax.imshow(data, cmap=colormap, vmin=vmin, vmax=vmax)
    ax.invert_yaxis()
    plt.colorbar(heatmap)


if __name__ == "__main__":
    FIGURES_DIR = Path("reports/figures")

    args = parse_args()
    ref_data = read_data(args.reference)
    samples = read_data(args.samples)
    predictions = read_data(args.predictions)
    if args.target is None:
        args.target = FIGURES_DIR / Path(
            f"{args.reference.stem}_{args.predictions.stem}{_TARGET_SUFFIX}"
        )
    args.target = args.target.with_suffix(".png")

    data_ratio = (samples.size - np.count_nonzero(np.isnan(samples))) / samples.size
    difference = predictions - ref_data
    mse = np.sum(np.square(difference)) / difference.size
    max_absolute_difference = np.absolute(difference).max()

    fig, axs = plt.subplots(nrows=2, ncols=2)
    fig.tight_layout()

    x, y = samples.nonzero()
    axs[0][0].set_title(
        f"Basis of prediction ({data_ratio*100:.2f}% of reference data)"
    )
    plot = axs[0][0].scatter(x, y, s=0.1, c=samples[x, y], cmap="jet")
    plt.colorbar(plot)

    show_heatmap(axs[1][0], ref_data, "Reference data")
    show_heatmap(axs[0][1], predictions, "Predicted data")
    # Range of values is set manually to ensure that 0 is the center and therefore will be
    # white in bwr colormap
    show_heatmap(
        axs[1][1],
        difference,
        f"Difference (MSE={mse:.2f})",
        "bwr",
        vmin=-max_absolute_difference,
        vmax=max_absolute_difference,
    )

    plt.savefig(args.target, bbox_inches="tight")
    if args.display:
        plt.show()
