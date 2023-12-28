from argparse import ArgumentParser
from pathlib import Path
from src.util.data_io import read_data, write_data
from src.util.cli import limited_float
from src.util.data import subsample

_TARGET_SUFFIX = "_subsampled"


def parse_args():
    parser = ArgumentParser(
        description="Subsample data and save results in another file"
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="File containing data to be subsampled",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        default=None,
        help=f"""File to save results in. If omitted results will be saved in the same directory as
        `data` under name '<data>{_TARGET_SUFFIX}'""",
    )
    parser.add_argument(
        "-r",
        "--ratio",
        type=limited_float(0.0, 1.0),
        default=0.1,
        help="""Part of data points in `data` that should be sampled. Needs to be in range
        (0.0, 1.0)""",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=None,
        help="Seed to use for RNG used in subsampling",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.target is None:
        args.target = args.data.with_stem(args.data.stem + _TARGET_SUFFIX)
    data = read_data(args.data)
    subsampled = subsample(data, args.ratio, args.seed)
    write_data(args.target, subsampled)
