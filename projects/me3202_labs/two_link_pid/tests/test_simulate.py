import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulate import inertia_matrix, simulate  # noqa: E402


class ArmTests(unittest.TestCase):
    def test_inertia_is_positive_definite(self):
        for angle in (-3.14, -1.0, 0.0, 1.0, 3.14):
            m11, m12, m22 = inertia_matrix(angle)
            self.assertGreater(m11, 0)
            self.assertGreater(m11 * m22 - m12 * m12, 0)

    def test_controller_tracks_both_joints(self):
        rows = simulate()
        last = rows[-1]
        self.assertLess(abs(last[1] - last[3]), 0.03)
        self.assertLess(abs(last[2] - last[4]), 0.03)
        self.assertTrue(all(abs(row[5]) <= 15 and abs(row[6]) <= 15 for row in rows))

    def test_invalid_time(self):
        with self.assertRaises(ValueError):
            simulate(duration=0)


if __name__ == "__main__":
    unittest.main()
