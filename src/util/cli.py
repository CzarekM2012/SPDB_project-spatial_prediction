import argparse

from numpy import inf


def limited_float(
    low: float = -inf,
    high: float = inf,
    low_inclusive: bool = False,
    high_inclusive: bool = False,
):
    """
    Check if passed string is a number in specified range

    Args:
        low (float, optional): Lower bound of range. Defaults to -inf.
        high (float, optional): Higher bound of range. Defaults to inf.
        low_inclusive (bool, optional): Is lower bound inclusive. Defaults to False.
        high_inclusive (bool, optional): Is higher bound inclusive. Defaults to False.

    Returns:
        Callable[[str], float]: Function converting string to float. It raises
        argparse.ArgumentTypeError if passed string can not be converted to a number in specified
        range
    """

    def convert(x: str):
        try:
            val = float(x)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"{x} is not a floating point number"
            ) from exc

        low_satisfied, opening_parenthesis = (
            (low <= val, "[") if low_inclusive else (low < val, "(")
        )
        high_satisfied, closing_parenthesis = (
            (high >= val, "]") if high_inclusive else (high > val, ")")
        )

        if not (low_satisfied and high_satisfied):
            raise argparse.ArgumentTypeError(
                f"{val} is not in range {opening_parenthesis}{low}, {high}{closing_parenthesis}"
            )
        return val

    return convert
