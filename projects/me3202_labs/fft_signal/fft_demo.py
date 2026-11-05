"""ME3202 Lab 3 study: compute a DFT of a generated two-tone signal."""

from __future__ import annotations

import cmath
import csv
import math
from pathlib import Path


def generated_signal(sample_rate_hz: int = 64, samples: int = 128) -> list[float]:
    if sample_rate_hz <= 0 or samples <= 0:
        raise ValueError("sample rate and sample count must be positive")
    return [
        math.sin(2 * math.pi * 5 * n / sample_rate_hz)
        + 0.5 * math.sin(2 * math.pi * 12 * n / sample_rate_hz)
        for n in range(samples)
    ]


def dft_magnitudes(signal: list[float], sample_rate_hz: float) -> list[tuple[float, float]]:
    if not signal or sample_rate_hz <= 0:
        raise ValueError("signal and sample rate must be valid")
    count = len(signal)
    result = []
    for bin_index in range(count // 2 + 1):
        coefficient = sum(
            value * cmath.exp(-2j * math.pi * bin_index * n / count)
            for n, value in enumerate(signal)
        )
        magnitude = abs(coefficient) / count
        if bin_index not in (0, count // 2):
            magnitude *= 2
        result.append((bin_index * sample_rate_hz / count, magnitude))
    return result


def main() -> None:
    sample_rate_hz = 64
    signal = generated_signal(sample_rate_hz)
    spectrum = dft_magnitudes(signal, sample_rate_hz)
    destination = Path(__file__).resolve().parent / "results" / "spectrum.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("frequency_hz", "magnitude"))
        writer.writerows(spectrum)
    peaks = sorted(spectrum[1:], key=lambda item: item[1], reverse=True)[:2]
    print(f"Frequency resolution: {sample_rate_hz / len(signal):.2f} Hz")
    print("Strongest peaks: " + ", ".join(f"{f:.1f} Hz ({m:.2f})" for f, m in peaks))
    print(f"CSV: {destination}")


if __name__ == "__main__":
    main()
