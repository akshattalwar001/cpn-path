"""Module to calculate pi to the 5th decimal digit using the Leibniz series."""


def calculate_pi(precision=5):
    """Calculate pi to the specified number of decimal digits using the Leibniz series.

    The Leibniz formula: pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...

    Args:
        precision: Number of decimal digits to round to (default 5).

    Returns:
        Pi rounded to the given number of decimal digits.
    """
    pi = 0.0
    sign = 1
    denominator = 1
    # The Leibniz series converges slowly, so we use a large number of iterations
    for _ in range(10_000_000):
        pi += sign * (4.0 / denominator)
        sign *= -1
        denominator += 2
    return round(pi, precision)


if __name__ == "__main__":
    print(f"Pi to 5 decimal places: {calculate_pi()}")
