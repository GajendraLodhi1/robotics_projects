import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulator import simulate  # noqa: E402


class CleaningBotTests(unittest.TestCase):
    def test_covers_all_reachable_cells_without_crossing_walls(self):
        grid = ("...#", ".#..", "....")
        report = simulate(grid, (0, 0))
        self.assertEqual(len(report.cleaned), report.reachable_count)
        self.assertEqual(report.coverage_percent, 100.0)
        self.assertTrue(all(grid[y][x] == "." for x, y in report.path))
        self.assertTrue(all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(report.path, report.path[1:])))

    def test_reports_unreachable_floor_separately(self):
        report = simulate((".#.", "###", ".#."), (0, 0))
        self.assertEqual(report.reachable_count, 1)
        self.assertEqual(report.open_count, 4)

    def test_rejects_nonrectangular_map(self):
        with self.assertRaises(ValueError):
            simulate(("...", ".."))


if __name__ == "__main__":
    unittest.main()
