import argparse


def limited_float(low: float, high: float):
    def convert(x: str):
        try:
            val = float(x)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"{x} is not a floating point number"
            ) from exc
        if not low < val < high:
            raise argparse.ArgumentTypeError(f"{val} is not in range ({low}, {high})")
        return val

    return convert
