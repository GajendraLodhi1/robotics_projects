"""ME3202 Lab 9 study: root locus for 1/(s^2 + 3s + 2)."""

from __future__ import annotations

import cmath
import csv
from pathlib import Path


def closed_loop_poles(gain: float) -> tuple[complex, complex]:
    if gain < 0:
        raise ValueError("This demo uses nonnegative proportional gain")
    discriminant = 1 - 4 * gain
    root = cmath.sqrt(discriminant)
    return ((-3 + root) / 2, (-3 - root) / 2)


def main() -> None:
    destination = Path(__file__).resolve().parent / "results" / "root_locus.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    gains = [step * 0.05 for step in range(201)]
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("gain", "pole_1_real", "pole_1_imag", "pole_2_real", "pole_2_imag"))
        for gain in gains:
            p1, p2 = closed_loop_poles(gain)
            writer.writerow((gain, p1.real, p1.imag, p2.real, p2.imag))
    for gain in (0, 0.25, 1):
        print(f"K={gain:.2f}: poles={closed_loop_poles(gain)}")
    print(f"CSV: {destination}")


if __name__ == "__main__":
    main()
