import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fft_demo import dft_magnitudes, generated_signal  # noqa: E402


class DftTests(unittest.TestCase):
    def test_two_expected_peaks(self):
        spectrum = dft_magnitudes(generated_signal(), 64)
        peaks = sorted(spectrum[1:], key=lambda item: item[1], reverse=True)[:2]
        self.assertEqual({round(f) for f, _ in peaks}, {5, 12})
        self.assertAlmostEqual(peaks[0][1], 1, places=6)
        self.assertAlmostEqual(peaks[1][1], 0.5, places=6)

    def test_invalid_rate(self):
        with self.assertRaises(ValueError):
            dft_magnitudes([1.0], 0)


if __name__ == "__main__":
    unittest.main()
