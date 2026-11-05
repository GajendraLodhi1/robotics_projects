import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from root_locus_demo import closed_loop_poles  # noqa: E402


class RootLocusTests(unittest.TestCase):
    def test_open_loop_poles(self):
        self.assertEqual(set(closed_loop_poles(0)), {-1 + 0j, -2 + 0j})

    def test_breakaway_gain(self):
        self.assertEqual(closed_loop_poles(0.25), (-1.5 + 0j, -1.5 + 0j))

    def test_positive_gains_remain_stable(self):
        for gain in (0, 0.1, 0.25, 1, 10):
            self.assertTrue(all(p.real < 0 for p in closed_loop_poles(gain)))


if __name__ == "__main__":
    unittest.main()
